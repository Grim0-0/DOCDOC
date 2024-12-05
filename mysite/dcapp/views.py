from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import DocumentForm, SignupForm, LoginForm, ClassifyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView 
from django.contrib.auth.views import PasswordChangeDoneView 
from PIL import Image
from paddleocr import PaddleOCR
import requests
import os
import re
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.utils.safestring import mark_safe
from .model_utils import model
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .model_utils import predict, load_and_preprocess_image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
def base(request):
    return render(request, 'base.html')

def user_profile(request):
    return render(request, 'registration/profile.html')

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('base')
    
class DashboardView(LoginRequiredMixin, View):
    login_url = 'registration/login/'  
    redirect_field_name = 'dashnext'  

    def get(self, request):
        return render(request, 'registration/dashboard.html', {'user': request.user})

class AboutView(TemplateView):
    template_name = 'about.html'

class readmore_view(TemplateView):
    template_name ='readmore_classify.html'

class readmoreview(TemplateView):
    template_name ='readmore_extract.html'

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        return super().form_valid(form)

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add custom context or perform actions after a successful password change
        context['custom_message'] = 'Your password has been successfully changed.'
        return context
    
def clean_text(text):
    # Normalize unicode characters to ASCII
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Common OCR misreads and corrections
    text = text.replace("‘", "'")  # Commonly misread single quote
    text = text.replace("’", "'")  # Commonly misread single quote
    text = text.replace("“", '"')  # Commonly misread double quote
    text = text.replace("”", '"')  # Commonly misread double quote
    text = text.replace("—", "-")  # Long dash to short dash
    text = text.replace("–", "-")  # En dash to hyphen
    
    # Replace OCR misreads of similar looking characters
    text = re.sub(r'\b1\b', 'I', text)  # OCR misread '1' as 'I'
    text = re.sub(r'\b0\b', 'O', text)  # OCR misread '0' as 'O'
    
    # Additional specific corrections
    text = re.sub(r'\bIll\b', 'III', text)  # Correct 'Ill' to 'III' if applicable
    text = re.sub(r'\bll\b', 'II', text)    # Correct 'll' to 'II' if applicable
    
    # Remove any leading/trailing special characters
    text = re.sub(r'^[^\w]+|[^\w]+$', '', text)
    
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Further sanitize for HTML rendering if needed
    text = re.sub(r'&', '&amp;', text)
    text = re.sub(r'<', '&lt;', text)
    text = re.sub(r'>', '&gt;', text)
    
    return text.strip()

def is_table_like(text_blocks):
    """
    Heuristic to determine if OCR results resemble a table structure.
    Assume it's a table if multiple rows have text aligned in similar column positions.
    """
    column_threshold = 3  # Minimum columns to consider it a table
    row_positions = {}

    for text, bbox in text_blocks:
        bottom_y = bbox[3][1]  # Use the bottom y-coordinate of the bounding box
        if bottom_y in row_positions:
            row_positions[bottom_y].append((bbox[0][0], text))  # Append start x-coordinate and text
        else:
            row_positions[bottom_y] = [(bbox[0][0], text)]

    # Check if there are multiple rows with enough columns
    table_like_rows = 0
    for positions in row_positions.values():
        if len(positions) >= column_threshold:
            table_like_rows += 1

    return table_like_rows > 1  # More than one row with sufficient columns

def extract_table_data(text_blocks):
    # Grouping text blocks by their y-coordinate to identify rows
    rows = {}
    y_tolerance = 10  # You can adjust this tolerance based on your OCR output specifics

    for text, bbox in text_blocks:
        # Calculate the central y-coordinate of the bounding box
        central_y = (bbox[1][1] + bbox[3][1]) // 2
        found_row = False

        # Check if this text belongs to an existing row
        for key in list(rows.keys()):
            if abs(key - central_y) < y_tolerance:
                rows[key].append((bbox[0][0], text))  # Append to existing row
                found_row = True
                break
        
        if not found_row:
            # Create a new row if no existing row is close enough
            rows[central_y] = [(bbox[0][0], text)]

    # Now sort rows and organize columns
    sorted_rows = sorted(rows.items(), key=lambda x: x[0])
    table_data = []

    for _, row in sorted_rows:
        # Sort each row's elements by their x-coordinate
        sorted_row = sorted(row, key=lambda x: x[0])
        table_data.append([text for _, text in sorted_row])

    return table_data


def format_as_html_table(table_data):
    """
    Convert structured table data into an HTML table directly.
    This method uses simple string manipulation to create an HTML representation of the table.
    """
    html = '<table border="1" class="table table-striped">'  # Start table tag with border and Bootstrap class for styling
    for row in table_data:
        html += '<tr>'  # Start a new row
        for cell in row:
            html += f'<td>{cell}</td>'  # Add each cell to the row
        html += '</tr>'  # End the row
    html += '</table>'  # End the table tag
    return html

from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)
@login_required
@never_cache
def extract_text_or_table(request):
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            image_path = document.image.path
            print(f"Debug: Processing image at {image_path}")
            ocr = PaddleOCR(use_angle_cls=True, lang='en')
            results = ocr.ocr(image_path, cls=True)

            # Prepare text_blocks from OCR results
            text_blocks = [(clean_text(line[1][0]), line[0]) for line in results for line in line]
            if is_table_like(text_blocks):
                table_data = extract_table_data(text_blocks)
                extracted_data = format_as_html_table(table_data)
                request.session['extracted_table'] = extracted_data
                
            else:
                extracted_data = "Detected as Text:\n" + "\n".join([block[0] for block in text_blocks])
                
            request.session['extracted_text'] = extracted_data
            request.session.modified = True
            return redirect(reverse('extract_text_done'))
    else:
        form = DocumentForm()
    response = render(request, 'extract_text.html', {'form': form})
    if not isinstance(response, HttpResponse):
        logger.error(f"Expected HttpResponse, got {type(response).__name__}")
    return response

@login_required
@never_cache
def extract_text_done(request):
    extracted_text = request.session.get('extracted_text', 'No text extracted or text lost.')
    safe_text = mark_safe(extracted_text)  # Marks the HTML as safe for rendering
    return render(request, 'extract_text_done.html', {'extracted_text': safe_text})

@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ClassifyDocumentView(View):
    def post(self, request):
        form = ClassifyForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES.get('file')
            if not image_file:
                return JsonResponse({'error': "No file was uploaded"}, status=400)
            
            # Save the uploaded file and generate a URL
            file_name = default_storage.save(image_file.name, ContentFile(image_file.read()))
            full_path = default_storage.path(file_name)

            # Convert TIFF to PNG if necessary
            if file_name.lower().endswith('.tif') or file_name.lower().endswith('.tiff'):
                png_file_name = os.path.splitext(file_name)[0] + '.png'
                png_full_path = default_storage.path(png_file_name)
                self.convert_tiff_to_png(full_path, png_full_path)
                file_name = png_file_name
                os.remove(full_path)  # Remove the original TIFF file

            image_url = default_storage.url(file_name)
        
            encoded_inputs = load_and_preprocess_image(image_file)
            if encoded_inputs is None:
                return JsonResponse({'error': "Error processing the image"}, status=400)
        
            predicted_class = predict(encoded_inputs)
            if predicted_class is None:
                return JsonResponse({'error': "Error during prediction"}, status=500)
        
            return render(request, 'classify_document_done.html', {
                'predicted_class': predicted_class,
                'image_url': image_url
                })
        else:
            return JsonResponse({'error': form.errors}, status=400)
        
    def convert_tiff_to_png(self, tiff_path, output_path):
        with Image.open(tiff_path) as img:
            img.convert('RGB').save(output_path, 'PNG')


    def get(self, request):
        if request.user.is_authenticated:
            form = ClassifyForm()
            return render(request, 'classify_document.html', {'form': form})
        else:
            return JsonResponse({'error': 'Access forbidden'}, status=403)
        
def display_result(request):
    # Assuming the result is stored in the session after classification
    predicted_class = request.session.get('predicted_class', 'No classification found')
    image_url = default_storage.url(file_name) # type: ignore
    # Alternatively, if you're passing the result as a query parameter
    # predicted_class = request.GET.get('result', 'No classification found')

    return render(request, 'classify_document_done.html', {
        'predicted_class': predicted_class,
        'image_url': image_url,
        })

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('login')
    return render(request, 'registration/delete_account.html')
