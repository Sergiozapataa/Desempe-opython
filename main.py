from flask import Flask, render_template_string, send_from_directory
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Cargar y procesar datos
archivo = "ventas_guacamole_mayo.xlsx"
df = pd.read_excel(archivo)

# Crear gráficas en la raíz del proyecto
def generar_graficas():
    verde = "#b6bb18"
    cafe = "#773611"

    # Total de ventas por producto
    ventas_producto = df.groupby("Producto")["Precio"].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=ventas_producto.values, y=ventas_producto.index, color=verde)
    plt.title("Total de ventas por Producto", color=cafe)
    plt.xlabel("Pesos COP", color=cafe)
    plt.ylabel("Producto", color=cafe)
    plt.xticks(color=cafe)
    plt.yticks(color=cafe)
    plt.tight_layout()
    plt.savefig("ventas_producto.png")
    plt.close()

    # Total de ventas por día
    ventas_dia = df.groupby("Fecha")["Precio"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=ventas_dia.index.strftime('%Y-%m-%d'), y=ventas_dia.values, color=verde)
    plt.title("Total de ventas por día", color=cafe)
    plt.xlabel("Fecha", color=cafe)
    plt.ylabel("Pesos COP", color=cafe)
    plt.xticks(rotation=45, color=cafe)
    plt.yticks(color=cafe)
    plt.tight_layout()
    plt.savefig("ventas_dia.png")
    plt.close()

    # Clientes con más productos comprados
    cliente_top = df["Cliente"].value_counts().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=cliente_top.values, y=cliente_top.index, color=verde)
    plt.title("Clientes con más productos comprados", color=cafe)
    plt.xlabel("Cantidad de productos", color=cafe)
    plt.ylabel("Cliente", color=cafe)
    plt.xticks(color=cafe)
    plt.yticks(color=cafe)
    plt.tight_layout()
    plt.savefig("clientes_top.png")
    plt.close()

    # Distribución de productos vendidos 
    productos = df["Producto"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(productos.values, labels=productos.index, autopct="%1.1f%%",
            startangle=140, colors=[verde, cafe] + ['#cccccc'] * (len(productos) - 2))
    plt.title("Distribución de productos vendidos", color=cafe)
    plt.tight_layout()
    plt.savefig("productos_pie.png")
    plt.close()

generar_graficas()

@app.route("/")
def index():
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    return render_template_string(html)


@app.route("/<path:filename>")
def custom_static(filename):
    return send_from_directory(".", filename)

if __name__ == "__main__":
    app.run(debug=True)
