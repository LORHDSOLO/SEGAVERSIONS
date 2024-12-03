document.getElementById("agregar-participante").addEventListener("click", function() {
    const lista = document.getElementById("lista-participantes");
    const input = document.createElement("input");
    input.type = "text";
    input.name = "participante";
    input.required = true;
    lista.appendChild(input);
});
