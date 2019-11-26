
const search = document.getElementById('query');

search.addEventListener('input', response);

async function response(evt) {
    const search = document.getElementById('query');
    console.log(search.value);
    const result = await fetch(`/live_search?query=${search.value}`);
    const data = await result.json();
    console.log("**", data);

    Object.keys(data).forEach(key => {
        let obj = data[key]
        let park = obj.park
        let name = obj.name
        let id = obj.id
        let campsite_list = document.getElementById("campsite_list");
        let display = `<div class="list" id="campsite"><div class="campsite-name"><input type="radio" name="selected_site" value=${id} required><b>${name}</b><br>${park}<br></div></div>`;
        $('#campsite_list').html(display);

    })
}

