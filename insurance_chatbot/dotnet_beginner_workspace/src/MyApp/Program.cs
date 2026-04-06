using System;

namespace MyApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Starting MyApp...");

            var service = new MyService();
            var name = args.Length > 0 ? args[0] : "World";
            var greeting = service.GetGreeting(name);

            Console.WriteLine(greeting);
            Console.WriteLine("Press Enter to exit...");
            Console.ReadLine();
        }
    }
}
