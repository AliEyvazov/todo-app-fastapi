# To-Do API (FastAPI & SQLAlchemy)

Bu layihə tam funksional Backend API sistemidir.

## Texnologiyalar
* **Python 3.11**
* **FastAPI**
* **SQLAlchemy** 
* **SQLite** 
* **Pydantic** 
* **JWT (JSON Web Tokens)** 

## Əsas Xüsusiyyətlər
* **Təhlükəsiz İstifadəçi Sistemi:** Şifrələrin `Passlib` (Bcrypt) vasitəsilə birtərəfli həşlənməsi (Hashing).
* **Token-based Authentication:** JWT ilə statussuz (stateless) sessiya idarəetməsi.
* **CRUD Əməliyyatları:** Tapşırıqların tam həyat dövrü (Yaratmaq, Oxumaq, Yeniləmək, Silmək).
* **Verilənlər Bazası Versiyalaşdırılması:** Alembic vasitəsilə məlumat itkisi olmadan miqrasiyaların aparılması.

## Quraşdırma və İşə Salma (Quick Start)

Layihəni lokal mühitdə işə salmaq üçün aşağıdakı addımları izləyin:

1. **Repozitoriyanı klonlayın:**
   ```bash
   git clone https://github.com/AliEyvazov/todo-app-fastapi.git
   cd todo-app-fastapi

2. **Virtual mühit yaradın və aktivləşdirin**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

3. **Asılılıqları yükləyin**:
   ```bash
   pip install -r requirements.txt

4. **Serveri işə salın**:
   ```bash
   uvicorn main:main:app --reload

http://127.0.0.1:8000/docs

## Müəllif
[AliEyvazov](https://github.com/AliEyvazov)
