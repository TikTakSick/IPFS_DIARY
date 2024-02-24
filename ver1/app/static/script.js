function get_dairy_content(ipfs_content_url){
	fetch(ipfs_content_url)
	.then(response => response.json()) // (2) レスポンスデータを取得
	.then(data => { // (3)レスポンスデータを処理
        console.log(data["dairy_content"])
        return data["dairy_content"]
	});
};

