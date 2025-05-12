import pytest
from unittest.mock import patch, MagicMock
from app.google_drive import upload_to_drive

@patch('app.google_drive.build')
@patch('app.google_drive.MediaFileUpload')
@patch('app.google_drive.os.path.exists', return_value=True)
@patch('app.google_drive.Credentials.from_authorized_user_file')
def test_upload_to_drive(mock_creds_loader, mock_exists, mock_media, mock_build):
    # Preparar mocks
    mock_creds = MagicMock()
    mock_creds.valid = True
    mock_creds_loader.return_value = mock_creds

    mock_service = MagicMock()
    mock_build.return_value = mock_service

    mock_files = mock_service.files.return_value
    mock_create = mock_files.create.return_value
    mock_create.execute.return_value = {'id': 'fake-file-id'}

    # Ejecutar función
    upload_to_drive('/fake/path/documento.txt', 'documento.txt')

    # Verificar llamadas clave
    mock_media.assert_called_once_with('/fake/path/documento.txt', resumable=True)
    mock_files.create.assert_called_once()
    mock_create.execute.assert_called_once()
