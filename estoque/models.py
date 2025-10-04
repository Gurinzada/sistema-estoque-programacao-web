from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key= True);
    name = models.CharField(max_length=150);
    jobTitle = models.CharField(max_length=100);
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        COLLABORATOR = 'COLLABORATOR', 'Colaborador'

    role = models.CharField(choices=Role.choices, default=Role.COLLABORATOR);
    email = models.EmailField(unique=True);
    password = models.CharField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.name}, ({self.jobTitle}) - {self.role}"

class Category(models.Model):
    id = models.AutoField(primary_key=True);
    name = models.CharField(max_length=150, unique=True);
    description = models.CharField(max_length=250);

    def __str__(self):
        return f"ID: {self.id} - {self.name}\n Descrição: {self.description}"

class Product(models.Model):
    id = models.AutoField(primary_key=True);
    name = models.CharField(max_length=150);
    description = models.CharField(max_length=250);
    quatityStock = models.IntegerField();
    costPrice = models.DecimalField(decimal_places=2, max_digits=10);
    salePrice = models.DecimalField(decimal_places=2, max_digits=10);
    createdAt = models.DateTimeField(auto_now_add=True);
    updatedAt = models.DateTimeField(auto_now=True);
    deletedAt = models.DateTimeField(null=True);
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products');

    def __str__(self):
        return f"ID: {self.id} - {self.name}\n Descrição: {self.description}\n Quantidade em estoque: {self.quatityStock}\n Preço de custo: {self.costPrice}\n Preço de venda: {self.salePrice}"

class MovementStock(models.Model):
    id = models.AutoField(primary_key=True);
    class Type(models.TextChoices):
        ENTRADA = 'ENTRADA' ,'Entrada'
        SAIDA = 'SAIDA', 'Saída'
    
    type = models.CharField(choices=Type.choices, default=Type.ENTRADA)
    date = models.DateTimeField()
    quantity = models.IntegerField()
    productId = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements');
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movements');
    createdAt = models.DateTimeField(auto_now_add=True);
    updatedAt = models.DateTimeField(auto_now=True);
    deletedAt = models.DateTimeField(null=True);

    def __str__(self):
        return f"ID: {self.id} - {self.type}\n Data da Movimentação: {self.date}\n Quantidade: {self.quantity}"

class Supplier(models.Model):
    id = models.AutoField(primary_key=True);
    name = models.CharField();
    cnpj = models.CharField(max_length=18, unique=True);
    email = models.EmailField(unique=True);
    phone = models.CharField(max_length=15);
    address = models.CharField();
    products = models.ManyToManyField(Product, related_name='suppliers');
    createdAt = models.DateTimeField(auto_now_add=True);
    updatedAt = models.DateTimeField(auto_now=True);
    deletedAt = models.DateTimeField(null=True);

    def __str__(self):
        return f"ID: {self.id} - {self.name}\n CNPJ: {self.cnpj}\n Email: {self.email}\n Telefone: {self.phone}\n Endereço: {self.address}"




