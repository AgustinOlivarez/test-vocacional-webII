document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("test-form");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const inputs = form.querySelectorAll("input, select, textarea");
    let vacios = false;
    let edad = null;

    inputs.forEach((input) => {
      const valor = input.value.trim();
      if (input.hasAttribute("required") && !valor) {
        vacios = true;
      }
      if (input.name.toLowerCase().includes("edad")) {
        edad = parseInt(valor);
      }
    });

    if (vacios) {
      Swal.fire({
        icon: "warning",
        title: "Campos incompletos",
        text: "Por favor, completá todos los campos requeridos.",
      });
      return;
    }

    if (edad !== null && (isNaN(edad) || edad < 16)) {
      Swal.fire({
        icon: "error",
        title: "Edad no válida",
        text: "Debés tener al menos 16 años para continuar.",
      });
      return;
    }

    Swal.fire({
      title: "¿Confirmar envío?",
      text: "¿Deseás enviar este formulario?",
      icon: "question",
      showCancelButton: true,
      confirmButtonText: "Sí, enviar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        const formData = new FormData(form);
        fetch(form.action, {
          method: "POST",
          body: formData,
          headers: { "X-Requested-With": "XMLHttpRequest" },
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Respuesta del servidor:", data);

            if (data.error) {
              Swal.fire({
                icon: "error",
                title: "Error",
                text: data.error,
              });
              return;
            }

            // Mostrar secciones
            document.getElementById("resultado-section").style.display = "grid";
            document.getElementById("carreras-section").style.display = "grid";

            // Mostrar descripción
            document.getElementById("resultado-descripcion").innerHTML = `
              <p><strong>Tu perfil profesional es: ${data.area}</strong></p>
              <p>${data.descripcion}</p>
              <p>${data.descripcion_traducida}</p>
            `;

            // Mostrar carreras recomendadas
            const lista = data.carreras
              .map((carrera, i) => {
                const traduccion = data.carreras_traducidas[i] || "";
                return `<label><input type="radio" name="curso"> ${carrera} — <em>${traduccion}</em></label>`;
              })
              .join("");

        document.getElementById("carreras-lista").innerHTML = `
          <p><strong>Los cursos que te recomendamos son:</strong></p>
          ${lista}
          <button class="btn">INSCRIBIRME</button>
        `;

            Swal.fire({
              icon: "success",
              title: "¡Formulario enviado!",
              text: `Gracias ${data.nombre}, descubrí tu perfil abajo.`,
              confirmButtonText: "Ver resultado",
            });
          })
          .catch(() => {
            Swal.fire({
              icon: "error",
              title: "Error",
              text: "Ocurrió un problema al enviar el formulario.",
            });
          });
      }
    });
  });
});
