/*!
    * Start Bootstrap - SB Admin v7.0.3 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2021 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
//

const obtener_view_actual = () => {
    const info_view_actual = $('#view-actual');
    return info_view_actual.val();
}

const mostrar_menu = (selector) => {
    const nuevo_view_actual = $(`#${selector}`);
    const info_view_actual = $('#view-actual');
    $(`#${obtener_view_actual()}`).hide();
    nuevo_view_actual.show();
    info_view_actual.val(selector);
 };

 const cargar_menu = (option_menu, id_view_element) => {
    if (id_view_element !== 'view-cargar-audio') {
        const view_element = $(`#${id_view_element}`);
        view_element.hide();
    }
    if (id_view_element !== 'view-descargar-resultado') {
        option_menu.addEventListener('click', () => {
            mostrar_menu(id_view_element);
        });
    }
 }

const crear_paginacion = (id_paginacion, api_url) => {
    const tabla = $(`#${id_paginacion}`)
      .DataTable({
          scrollY: '200px',
          scrollCollapse: true,
          order: [[1, 'desc']],
          ajax: {
              url: api_url,
              dataSrc: 'results'
          },
          columns: [
              { 
                  data: 'nombre',
              },
              { 
                data: 'fecha',
                render: (data, type) => {
                    return new Date(data).toLocaleString();
                },
              },
            ],
        });
    tabla.on('click', 'tbody > tr', (event) => {
        //Si se presiona el elemento td, se obtiene el tr contenedor
        if(event.target.nodeName.toLowerCase()) {
            const view_actual = obtener_view_actual();
            const input_audio = $(`div#${view_actual} form div input.audio`);
            const td_archivo = $(event.target.parentNode.children[0]);
            const nombre_archivo = td_archivo.text();
            input_audio.val(nombre_archivo);
        }
    });
    return tabla;
}

const obtener_csrftoken = () => {
     return document.getElementsByName('csrfmiddlewaretoken')[0].value;
}

const enviar_formulario_caracteristica = (form) => {
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const data = new FormData(form);
        const action = form.action;
        const method = form.method;

        $.ajax({
            type: method,
            url: action,
            headers: {
                'X-CSRFToken': obtener_csrftoken()
            },
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            beforeSend: (jqXHR, settings) => {
                Swal.fire({
                    title: 'Extrayendo característica',
                    didOpen: () => {
                    Swal.showLoading()
                    }
                });
            }
        })
        .done(async (response) => {
            const view_actual = obtener_view_actual();
            const img = $(`div#${view_actual} div div img#visualizador`);
            const { png, pickle } = response;
            const fetchResponsePng = await fetch(`data:image/png;base64,${png}`);
            const fetchResponsePickle = await fetch(`data:image/png;base64,${pickle}`);
            const blobPng = await fetchResponsePng.blob();
            const blobPickle = await fetchResponsePickle.blob();
            const urlPickleAnterior = sessionStorage.getItem(`${view_actual}-pickle`);
            if (urlPickleAnterior) {
                window.URL.revokeObjectURL(urlPickleAnterior);
            }
            window.URL.revokeObjectURL(img.attr('src'));
            const urlPng = window.URL.createObjectURL(blobPng);
            const urlPickle = window.URL.createObjectURL(blobPickle);
            img.attr('src', urlPng);
            sessionStorage.setItem(`${view_actual}-png`, urlPng);
            sessionStorage.setItem(`${view_actual}-pickle`, urlPickle);
            Swal.close();
        })
        .fail((response) => {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Algo ha salido mal!. No se ha podido extraer la característica',
                showConfirmButton: false,
            });
        });
    })
}

const descargar_archivo = (tipo) => {
    const view_actual = obtener_view_actual();
    if (view_actual !== 'view-cargar-audio') {
        const url = sessionStorage.getItem(`${view_actual}-${tipo}`);
        if (url) {
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `resultado.${tipo}`;
            document.body.appendChild(a);
            a.click();
        }
    }
}

/*
    Se agregan funcionalidades a los elementos del DOM
*/

window.addEventListener('DOMContentLoaded', event => {
    //limpiar los archivos .png y .pickle que quedan luego de recargar la página
    sessionStorage.clear();
    
    //Cambia el comportamiento del formulario de características, para enviarlo a la api
    $.each($('div.menu:not(#view-cargar-audio) form'), (index, form) => {
        enviar_formulario_caracteristica(form);
    });

    //Se cargan las animaciones del menú, para ocultar y mostrar las opciones del menú
    $.each($('.menu-opcion'), (index, option_menu) => {
        const id_menu_element = $(option_menu).attr('id');
        const id_view_element = `view-${id_menu_element}`;
        cargar_menu(option_menu, id_view_element);
    });

    //Se crea la tabla con paginación
    const id_paginacion = 'paginacion';
    const api_url = $('#api-audios').val();
    const tabla = crear_paginacion(id_paginacion, api_url);

    //Se asigna la funcionalidad de descarga de archivos
    const descargar = $('#descargar');
    descargar.bind('click', (event) => {
        [$('input#png'), $('input#pickle')].forEach((value, index) => {
            if (value.prop('checked')) {
                descargar_archivo(value.attr('value'));
            }
        });
    });

    //Se modifica el comportamiento del formulario de carga de audio, para enviar los datos a la api
    const form_audio = document.getElementById('form_audio');
    form_audio.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const data = new FormData(form_audio);
        const url = form_audio.action;
        const method = form_audio.method;

        function generar_peticion (method) {
            return $.ajax({
                type: method,
                url: url,
                headers: {
                    'X-CSRFToken': obtener_csrftoken()
                },
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                beforeSend: (jqXHR, settings) => {
                    Swal.fire({
                        title: 'Cargando audio',
                        didOpen: () => {
                        Swal.showLoading()
                        }
                    });
                }
            }).done(function(response){
                Swal.close();            
                Swal.fire({
                    icon: 'success',
                    title: 'Exito!',
                    text: 'El archivo se ha cargado.',
                    showConfirmButton: false,
                  });
                tabla.ajax.reload();
            });
        }

        const cargar_audio = generar_peticion(method);
        
        cargar_audio
        .fail(function(response){
            if (response.status === 409) {
                Swal.fire({
                    title: 'Este archivo ya existe!',
                    text: "¿Quiere modificarlo?",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Modificar'
                  }).then((result) => {
                    if (result.isConfirmed) {
                        const modificar_audio = generar_peticion('PUT');
                        modificar_audio
                        .fail(function(response){
                            Swal.fire({
                                icon: 'error',
                                title: 'Oops...',
                                text: 'Algo ha salido mal!. No se ha podido cargar el audio',
                                showConfirmButton: false,
                            });
                        });
                    }
                  })
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Algo ha salido mal!. No se ha podido cargar el audio',
                    showConfirmButton: false,
                })
            }
        });
    });

    //Se agrega vista previa del audio (escuchar audio previo al envio)
    const input_audio = document.getElementById('audio_cargado');
    input_audio.addEventListener('change', (event) => {
        reproductor_audio = document.getElementById('reproductor');
        window.URL.revokeObjectURL(reproductor_audio.src);
        reproductor_audio.src = window.URL.createObjectURL(event.target.files[0]);
    });

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
});
