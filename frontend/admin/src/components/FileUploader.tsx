import { useState, ChangeEvent } from 'react';
import styled from 'styled-components';

const UploadContainer = styled.div`
  margin: 20px 0;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
`;

const FileInput = styled.input`
  padding: 0;
`;

interface FileUploaderProps {
  label: string;
  onChange: (file: File | null) => void;
}

export const FileUploader: React.FC<FileUploaderProps> = ({ label, onChange }) => {
  const [fileName, setFileName] = useState<string>('');

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setFileName(file ? file.name : '');
    onChange(file);
  };

  return (
    <UploadContainer>
      <Label>{label}</Label>
      <FileInput type="file" accept=".pdf" onChange={handleFileChange} />
      {fileName && <p>Selected: {fileName}</p>}
    </UploadContainer>
  );
};