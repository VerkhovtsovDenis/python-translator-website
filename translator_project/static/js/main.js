const all_td = document.getElementsByTagName('td');

for (let td of all_td) {
    td.onclick = () => {
        const content = td.textContent || td.innerText;
        navigator.clipboard.writeText(content)
            .then(() => {
                console.log('Содержимое скопировано в буфер обмена:', content);
            })
            .catch(err => {
                console.error('Ошибка при копировании:', err);
            });
    };
}
