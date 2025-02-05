
"""
Lee código QR a partir de 
imágenes o videos
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import cv2

# Lógica del programa
def cerrar_ventana():
	if messagebox.askokcancel("Salir", "¿Estás seguro de salir?"):
		ventana.destroy()

def mostrar_exito():
	messagebox.showinfo("Éxito", "Código QR leído exitosamente.")

def mostrar_advertencia():
    messagebox.showwarning("Advertencia", "Código QR inválido. Inténtalo de nuevo.")

def mostrar_error():
    messagebox.showerror("Error", "No se detectó un código QR.")

def procesar_imagen():
	try:
		imagen = filedialog.askopenfilename(title = "Abrir imagen con QR", initialdir = "C:", 
			filetypes = (("Icon", "*.png"), ("Icon", "*.ico"), ("Icon", "*.jpg")))

		detector = cv2.QRCodeDetector()
		valor_codigo = detector.detectAndDecode(cv2.imread(imagen))

		if valor_codigo[0]:
			mostrar_exito()
			mostrar_resultado(valor_codigo[0])
			return

		mostrar_advertencia()

	except Exception as e:
		mostrar_error()

def procesar_video():
    try:
        cap = cv2.VideoCapture(0)
        qr_detector = cv2.QRCodeDetector()

        while True:
            ret, frame = cap.read()
            if not ret: break

            valor, pts, _ = qr_detector.detectAndDecode(frame)
            if valor:
                cv2.polylines(frame, [pts.astype(int)], True, (0, 255, 0), 2)
                cv2.putText(frame, valor, tuple(pts[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2.imshow("QR Scanner", frame)
            if cv2.waitKey(1) & 0xFF == ord("x"): break

        cap.release()
        cv2.destroyAllWindows()

        if valor: # Solo mostrar si se detectó un QR
            mostrar_exito()
            mostrar_resultado(valor)
            return

        mostrar_advertencia()

    except Exception:
        mostrar_error()

def copiar_texto(ventana, etiqueta):
    # Copiar el texto del Label al portapapeles
    texto = etiqueta.cget("text") 
    ventana.clipboard_clear() # Limpiar el portapapeles
    ventana.clipboard_append(texto) # Copiar el texto al portapapeles

def mostrar_resultado(texto):
	ventana_resultado = tk.Tk()
	ventana_resultado.title("Resultado del código QR")
	ventana_resultado.config(bg = "#F3F4F6")
	ventana_resultado.geometry("350x350")
	ventana_resultado.resizable(0, 0)
	ventana_resultado.iconbitmap("Logo.ico")

	# Valor del código
	resultado_codigo = tk.Label(ventana_resultado, text = texto, 
		font = ("Times New Roman", 15), fg = "#1F2937", wraplength = 200)
	resultado_codigo.pack(pady = 30)

	tk.Button(ventana_resultado, text = "Copiar Resultado", font = ("Times New Roman", 12), 
	cursor = "hand2", bg = "#3B82F6", fg = "#1F2937", 
	command = lambda: copiar_texto(ventana_resultado, resultado_codigo)).pack(pady = 20)

	ventana_resultado.mainloop()

# Interfaz
ventana = tk.Tk()
ventana.title("Lector de código QR")
ventana.config(bg = "#F3F4F6")
ventana.geometry("400x400")
ventana.resizable(0, 0)
ventana.iconbitmap("Logo.ico")

# Títulos
tk.Label(ventana, text = "Lector de código QR", font = ("Times New Roman", 19), fg = "#1F2937").place(x = 95, y = 65)
tk.Label(ventana, text = "Selecciona el formato del código", font = ("Times New Roman", 19), fg = "#1F2937").place(x = 35, y = 100)

# Botones
tk.Button(ventana, text = "Imagen", font = ("Times New Roman", 19), 
	cursor = "hand2", bg = "#3B82F6", fg = "#1F2937", command = procesar_imagen).place(x = 80, y = 200)
tk.Button(ventana, text = "Vídeo", font = ("Times New Roman", 19), 
	cursor = "hand2", bg = "#3B82F6", fg = "#1F2937", command = procesar_video).place(x = 220, y = 200)

ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)
ventana.mainloop()