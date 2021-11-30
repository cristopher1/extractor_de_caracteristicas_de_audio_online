async function frontEnd() {
    let pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/"
    });
    await pyodide.loadPackage(["numpy", "matplotlib"])
    await pyodide.runPythonAsync(`
        import js
        import matplotlib.pyplot as plt
        import numpy as np

        #def reproducir_audio(event):
        #    print(event.target.files.to_py()[0])
        #    reproductor_audio = js.document.getElementById('reproductor')
        #    js.window.URL.revokeObjectURL(reproductor_audio.src)
        #    #reproductor_audio.src = js.window.URL.createObjectURL(event.target.files[0])
        
        #input_audio = js.document.getElementById('audio_cargado')
        #input_audio.addEventListener('change', reproducir_audio)
    `)
}

frontEnd();