using MyWebApi.Models;
using System.Collections.Concurrent;
using System.Collections.Generic;

namespace MyWebApi.Services
{
    public class InMemoryProductRepository : IProductRepository
    {
        private readonly ConcurrentDictionary<int, Product> _store = new();
        private int _nextId = 1;

        public InMemoryProductRepository()
        {
            // Seed with sample data
            Add(new Product { Name = "Widget", Description = "A basic widget", Price = 9.99M });
            Add(new Product { Name = "Gadget", Description = "A useful gadget", Price = 19.99M });
        }

        public Product Add(Product product)
        {
            var id = System.Threading.Interlocked.Increment(ref _nextId);
            product.Id = id;
            _store[id] = product;
            return product;
        }

        public bool Delete(int id)
        {
            return _store.TryRemove(id, out _);
        }

        public IEnumerable<Product> GetAll()
        {
            return _store.Values;
        }

        public Product? GetById(int id)
        {
            _store.TryGetValue(id, out var product);
            return product;
        }

        public bool Update(int id, Product product)
        {
            if (!_store.ContainsKey(id)) return false;
            product.Id = id;
            _store[id] = product;
            return true;
        }
    }
}
