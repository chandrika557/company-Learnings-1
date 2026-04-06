using MyWebApi.Models;
using System.Collections.Generic;

namespace MyWebApi.Services
{
    public interface IProductRepository
    {
        IEnumerable<Product> GetAll();
        Product? GetById(int id);
        Product Add(Product product);
        bool Update(int id, Product product);
        bool Delete(int id);
    }
}
