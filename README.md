# Florli
### AI-Powered Flower Classification & Virtual Gardening

Florli is a Django web application that combines artificial intelligence with gamified gardening. Users upload flower photos for AI classification, unlock plants in their virtual garden, and share knowledge with the community.

The system integrates machine learning models for plant identification and features an interactive virtual garden where users can plant and arrange their discovered flowers.

> **Note:** This is a university thesis project showcasing AI integration in web applications. The ML models are trained for educational purposes and may require optimization for production use.

> **Watch the Demo here**: [FlorliDemo](https://drive.google.com/drive/u/0/folders/110YWRq0WqZT1Qtg2l6fj6Sgfs-8D0ydL](https://drive.google.com/drive/u/0/folders/110YWRq0WqZT1Qtg2l6fj6Sgfs-8D0ydL))

### Features
- **AI Plant Classification**: Upload flower photos and get instant identification with confidence scores
- **Virtual Garden**: Interactive drag-and-drop garden where users can plant unlocked flowers
- **Community Blog**: Share plant discoveries, care tips, and gardening experiences  
- **Care Guides**: Detailed plant care instructions with difficulty ratings
- **Gamification**: Unlock new flowers through successful classifications and build your collection

### Technology Stack
- **Backend**: Django, Python
- **Frontend**: HTML/CSS/JavaScript, Bootstrap 4
- **AI/ML**: TensorFlow/Keras for plant classification
- **Database**: SQLite (development), PostgreSQL-ready
- **Image Processing**: Pillow for upload handling

> **Note:** The project includes pre-trained models for demonstration. For full functionality, ensure all model files are properly configured in the deployment environment.

### Model Architecture
- Currently using a **pre-trained EfficientNetB2** model for flower classification
- Model integrated within the `blog/` application
- Transfer learning approach for efficient flower species identification

### Quick Start
```bash
pip install -r requirements.txt
cd licenta_project
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
> **Note:** Use a python virtual environment

### Project Structure
- `blog/` - Main application with posts and community features
- `virtual_garden/` - Garden functionality and flower management
- `users/` - User authentication and profiles

> **Note:** The Model is integrated in blog/
