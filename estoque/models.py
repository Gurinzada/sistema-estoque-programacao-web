from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key= True);
    name = models.CharField(max_length=150);
    jobTitle = models.CharField(max_length=100);
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        COLLABORATOR = 'COLLABORATOR', 'Colaborador'

    role = models.CharField(choices=Role.choices, default=Role.COLLABORATOR, max_length=20);
    email = models.EmailField(unique=True, max_length=200);
    password = models.TextField()
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
    costPrice = models.DecimalField(decimal_places=2, max_digits=10, default=0);
    salePrice = models.DecimalField(decimal_places=2, max_digits=10, default=0);
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
    
    type = models.CharField(choices=Type.choices, default=Type.ENTRADA, max_length=10)
    date = models.DateTimeField()
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements');
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movements');
    createdAt = models.DateTimeField(auto_now_add=True);
    updatedAt = models.DateTimeField(auto_now=True);
    deletedAt = models.DateTimeField(null=True);

    def __str__(self):
        return f"ID: {self.id} - {self.type}\n Data da Movimentação: {self.date}\n Quantidade: {self.quantity}"

class Supplier(models.Model):
    id = models.AutoField(primary_key=True);
    name = models.CharField(max_length=150);
    cnpj = models.CharField(max_length=18, unique=True);
    email = models.EmailField(unique=True, max_length=150);
    phone = models.CharField(max_length=15, null=True);
    address = models.TextField();
    zipCode = models.CharField(max_length=9);
    products = models.ManyToManyField(Product, related_name='suppliers');
    createdAt = models.DateTimeField(auto_now_add=True);
    updatedAt = models.DateTimeField(auto_now=True);
    deletedAt = models.DateTimeField(null=True);

    def __str__(self):
        return f"ID: {self.id} - {self.name}\n CNPJ: {self.cnpj}\n Email: {self.email}\n Telefone: {self.phone}\n Endereço: {self.address}"




