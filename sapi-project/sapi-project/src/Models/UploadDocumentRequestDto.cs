namespace SapiProject.Models
{
    public class UploadDocumentRequestDto
    {
        public string? Document { get; set; }
        public string? FileName { get; set; }
        public string? ContentType { get; set; }
    }
}