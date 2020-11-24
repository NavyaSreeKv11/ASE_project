function popup(id0, id1, id2, download_img_id, download_img_url) {
    var modal = document.getElementById(id0);

    // Get the image and insert it inside the modal - use its "alt" text as a caption
    var img = document.getElementById(id1);
    var modalImg = document.getElementById(id2);
    var dwnld_img = document.getElementById(download_img_id);
    dwnld_img.setAttribute("href", download_img_url);
    img.onclick = function () {
        modal.style.display = "block";
        modalImg.src = this.src;
        captionText.innerHTML = this.alt;
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            }
    };

    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    };
}
