function openFolderDialog() {
    const input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('webkitdirectory', true);
    input.setAttribute('directory', true);
    input.addEventListener('change', handleFolderSelection);
    input.click();
}

function handleFolderSelection(event) {
    const input = event.target;
    const files = input.files;
    if (files.length > 0) {
        const folderPath = files[0].webkitRelativePath.split('/')[0];
        const lienField = document.querySelector('#id_lien');
        lienField.value = folderPath;
    }
}