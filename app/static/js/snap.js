// const to_image = (id) => {
//   let dom = import("./dom-to-image.js");
//   dom.toBlob(document.getElementById(id)).then(function (blob) {
//     window.saveAs(blob, "image.png");
//   });
// };
import domtoimage from "dom-to-image";

var scale = 6;
export const to_image = (id) => {
  domtoimage
    .toPng(id, {
      width: id.clientWidth * scale,
      height: id.clientHeight * scale,
      style: {
        transform: `scale(${scale})`,
        transformOrigin: "top left",
        width: id.clientWidth + "px", // use original width of DOM element to avoid part of the image being cropped out
        height: id.clientHeight + "px", // use original height of DOM element
      },
    })
    .then((dataUrl) => {
      // let image = new Image();
      window.saveAs(dataUrl, "image.png");
    });
};
