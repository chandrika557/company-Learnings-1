namespace MyApp
{
    /// <summary>
    /// Simple service used by the console app. Keeps logic separate from Program.
    /// </summary>
    public class MyService
    {
        public string GetGreeting(string name)
        {
            if (string.IsNullOrWhiteSpace(name))
                name = "World";
            return $"Hello, {name}! Welcome to your first .NET app.";
        }
    }
}
