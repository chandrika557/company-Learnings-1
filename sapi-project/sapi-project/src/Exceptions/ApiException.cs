using System;

namespace SapiProject.Exceptions
{
    public class ApiException : Exception
    {
        public string Code { get; }
        public int StatusCode { get; }

        public ApiException(string message, string code, int statusCode)
            : base(message)
        {
            Code = code;
            StatusCode = statusCode;
        }
    }
}