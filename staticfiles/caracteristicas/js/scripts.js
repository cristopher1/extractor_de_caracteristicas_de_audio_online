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

const cargar_paginacion = (id_paginacion_element, api_url) => {
    const tabla = $(`#${id_paginacion_element}`)
    .DataTable({
        scrollY: '200px',
        scrollCollapse: true,
        order: [[1, 'desc']],
        ajax: {
            url: api_url,
            dataSrc: 'results'
        },
        columns: [
            { data: 'nombre' },
            { 
                data: 'fecha',
                render: (data, type) => {
                    return new Date(data).toLocaleString();
                }
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
}

const obtener_csrftoken = () => {
     return document.getElementsByName('csrfmiddlewaretoken')[0].value;
}

const enviar_data_caracteristica = (form) => {
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
                    title: 'Generando características',
                    didOpen: () => {
                    Swal.showLoading()
                    }
                });
            }
        })
        .done(async (response) => {
            const view_actual = obtener_view_actual();
            const img = $(`div#${view_actual} div div img#visualizador`);
            const png = response.png
            const pickle = response.pickle
            const fetchResponsePng = await fetch(`data:image/png;base64,${png}`);
            const blobPng = await fetchResponsePng.blob();
            const fetchResponsePickle = await fetch(`data:image/png;base64,${pickle}`);
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

window.addEventListener('DOMContentLoaded', event => {
    sessionStorage.clear();
    $.each($('div.menu form'), (index, form) => {
        enviar_data_caracteristica(form);
    });
    $.each($('.menu-opcion'), (index, option_menu) => {
        const id_menu_element = $(option_menu).attr('id');
        const id_view_element = `view-${id_menu_element}`;
        const id_paginacion_element = `paginacion-${id_menu_element}`;
        const api_url = $('#api-audios').val();
        cargar_menu(option_menu, id_view_element);
        cargar_paginacion(id_paginacion_element, api_url);
    });

    const descargar = $('#descargar');
    descargar.bind('click', (event) => {
        const descarga = (tipo) => {
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
        [$('input#png'), $('input#pickle')].forEach((value, index) => {
            if (value.prop('checked')) {
                descarga(value.attr('value'));
            }
        });
    });

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
                Swal.fire({
                    icon: 'success',
                    title: 'Exito!',
                    text: 'El archivo se ha cargado.',
                    showConfirmButton: false,
                  });
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
