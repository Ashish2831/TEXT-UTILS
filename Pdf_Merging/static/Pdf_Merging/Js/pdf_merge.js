Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#one", {
  maxFiles: 10,
  maxFilesize: 5,
  acceptedFiles: ".pdf",
  dictDefaultMessage: 'Drap your files here sequentially',
});
