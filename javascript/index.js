
const onClickAdd = () => {
    const inputText = document.getElementById("add-text").value;
    document.getElementById("add-text").value = "";

    const li = document.createElement("li");
    const div = document.createElement("div");
    div.className = "list-row";

    const p = document.createElement("p");
    p.className = "todo-item";
    p.innerText = inputText;

    const completeButton = document.createElement("button");
    completeButton.innerText = "完了";
    completeButton.addEventListener("click", () => {alert("完了")})

    const deleteButton = document.createElement("button");
    deleteButton.innerText = "削除";
    deleteButton.addEventListener("click", () => {alert("削除")})


    div.appendChild(p);
    div.appendChild(completeButton);
    div.appendChild(deleteButton);


    li.appendChild(div);

    console.log(li);

    document.getElementById("incomplete-list").appendChild(li);


}

document.getElementById("add-button").addEventListener("click", onClickAdd);