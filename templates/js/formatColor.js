function background(poster_src) {
    var containerPpal = document.getElementById("containerPpal");
    urlPoster = "\https://image.tmdb.org/t/p/w1400_and_h450_face" + poster_src;
    containerPpal.style.display = "block";
    containerPpal.style.backgroundSize = "cover";
    containerPpal.style.backgroundRepeat = "no-repeat";
    containerPpal.style.backgroundImage = "url(" + urlPoster + ")";
     containerPpal.style.borderBottom = "2px solid";

    var rgb = getAverageRGB(document.getElementById('poster'));
    var divCustom = document.getElementById("custom_bg");
    divCustom.style.backgroundImage = "radial-gradient(circle at 20% 50%, rgba(" + rgb.r + "," + rgb.g + ", " + rgb.b + ", 0.90) 0%, rgba(" + rgb.r + ", " + rgb.g + ", " + rgb.g + ", 0.70) 100%)";
}

function getAverageRGB(imgEl) {
    var blockSize = 5,
        defaultRGB = {r: 0, g: 0, b: 0},
        canvas = document.createElement('canvas'),
        context = canvas.getContext && canvas.getContext('2d'),
        data, width, height,
        i = -4,
        length,
        rgb = {r: 0, g: 0, b: 0},
        count = 0;

    if (!context) {
        return defaultRGB;
    }
    height = canvas.height = imgEl.naturalHeight || imgEl.offsetHeight || imgEl.height;
    width = canvas.width = imgEl.naturalWidth || imgEl.offsetWidth || imgEl.width;
    context.drawImage(imgEl, 0, 0);
    data = context.getImageData(0, 0, width, height);
    length = data.data.length;
    while ((i += blockSize * 4) < length) {
        ++count;
        rgb.r += data.data[i];
        rgb.g += data.data[i + 1];
        rgb.b += data.data[i + 2];
    }
    rgb.r = ~~(rgb.r / count);
    rgb.g = ~~(rgb.g / count);
    rgb.b = ~~(rgb.b / count);
    return rgb;
}




