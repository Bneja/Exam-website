const adminPage = {
    template:/*html*/`
    <select v-model="selProductid" v-on:change="updateProdForm" v-if="admin">
        <option value="add">
            Add product
        </option>
        <option disabled></option>
        <option disabled>
            Edit product:
        </option>
        <option disabled></option>
        <option v-for="product in products" v-bind:value="product.id">
            {{product.name}}
        </option>
    </select>
    <div id="add-prod-container" v-if="admin">
        <form class="login-signup" v-on:submit.prevent="uploadProduct">
            <fieldset>
                <legend v-if="selProduct">Edit product</legend>
                <legend v-else>Add product</legend>
                <p class="error" v-if="errorMessage">{{errorMessage}}</p>
                <p class="success" v-if="message">{{message}}</p>
                <div class="input-container">
                    <label for="prodname">Name</label>
                    <input type="text" id="prodname" v-model="inpName">
                </div>
                <div class="input-container">
                    <label for="prodPrice">Price</label>
                    <input type="number" id="prodPrice" v-model="inpPrice">
                </div>
                <div class="input-container">
                    <label for="prodShortDesc">Short description</label>
                    <input type="text" id="prodShortDesc" v-model="inpShortDesc">
                </div>
                <div class="input-container">
                    <label for="prodImage">Image</label>
                    <input type="file" id="prodImage" accept=".png,.jpg" ref="inpImage" v-on:change="showImage">
                </div>                
                <div class="input-container">
                    <label for="prodDesc">Description</label>
                    <textarea id="prodDesc" v-model="inpDesc"></textarea>
                </div>
                <div class="input-container">
                    <input type="button" class="submit" value="Delete" v-if="selProduct" v-on:click="openDeleteModal">
                    <input type="submit" v-if="selProduct" class="submit" value="Edit">
                    <input type="submit" v-else class="submit" value="Add">
                </div>
            </fieldset>
        </form>
        <div>    
            Preview
            <article id="product-preview">
                <img class="prod-img" v-bind:src="imgPath"/>
                <div class="details-container">
                    <strong>{{inpName}}</strong>
                    <strong class="prod-price">{{inpPrice}}-&nbsp;kr</strong>
                    <span>{{inpShortDesc}}</span>
                </div>
            </article>
        </div>
        <dialog ref="deleteModal" id="delete-modal">
            <div id="inner-delete-modal">
                Are you sure you want to delete this product?
                <div>
                    <button v-on:click="closeDeleteModal">No</button>
                    <button v-on:click="deleteProduct">Yes</button>
                </div>
            </div>
        </dialog>
    </div>
    <p v-else>You do not have access to this page</p>
    <small v-if="admin">&nbsp;Browser caching might prevent the image to update clientside, you migth need to reload.</small>
    `,
    props: ["user"],
    data: function () {
        return {
            inpName: "",
            inpPrice: "",
            inpShortDesc: "",
            inpDesc: "",
            imgPath: "static/src/images/placeholder-image.png",
            errorMessage: "",
            message: "",
            file: null,
            selProduct: null,
            selProductid: "add",
            products: []
        }
    },
    methods: {
        showImage: function (event) {
            this.file = event.target.files[0]
            if (this.file && this.checkImage()) {
                this.imgPath = URL.createObjectURL(this.file)
            } else {
                this.$refs.inpImage.value=null
                this.file=""
                if (!this.selProduct){
                    this.imgPath = "static/src/images/placeholder-image.png"
                }
            }
        },
        checkImage: function () {
            if (!this.file) {
                this.errorMessage = "you must select an image"
                setTimeout(() => this.errorMessage = "", 4000)
                return false
            }
            const extension = this.file.name.split(".").at(-1).toLowerCase()
            if (extension !== "jpg" && extension !== "png") {
                this.errorMessage = "Image must be a jpg or png"
                setTimeout(() => this.errorMessage = "", 4000)
                return false
            }
            if (this.file.size > 100000) {
                this.errorMessage = "The image must be less than 100kb"
                setTimeout(() => this.errorMessage = "", 4000)
                return false
            }
            return true
        },
        uploadProduct: async function () {
            if (this.inpName && this.inpPrice !== "" && this.inpPrice > 0) {
                if (!this.selProduct || (this.selProduct && this.file)){
                    if (!this.checkImage()){
                        return
                    }
                }
                const formData = new FormData();
                formData.append("image", this.file);
                formData.append("name", this.inpName)
                formData.append("price", this.inpPrice)
                formData.append("shortdesc", this.inpShortDesc)
                formData.append("desc", this.inpDesc)
                let method
                let url
                if (this.selProduct) {
                    method = "PUT"
                    url = "/products/" + this.selProduct.id
                    formData.append('imagepath',this.selProduct.imgpath)
                } else {
                    method = "POST"
                    url = "/products"
                }
                let response = await fetch(url, {
                    method: method,
                    body: formData
                })
                if (response.status == 200) {
                    let result = await response.json()
                    this.message = result.message
                    setTimeout(() => this.message = "", 4000)
                    await this.getProducts()
                    this.updateProdForm()
                } else {
                    let result = await response.json()
                    this.errorMessage = result.message
                    setTimeout(() => this.errorMessage = "", 4000)
                }
            } else {
                this.errorMessage = "Name cannot be empty and price must be positive"
                setTimeout(() => this.errorMessage = "", 4000)
            }
        },
        openDeleteModal:function(){
            this.$refs.deleteModal.showModal()
        },
        closeDeleteModal:function(){
            this.$refs.deleteModal.close()
        },
        deleteProduct:async function(){
            let response = await fetch("/products/"+this.selProduct.id,{
                method:"DELETE"
            })
            this.closeDeleteModal()
            if (response.status==200){
                let result = await response.json()
                await this.getProducts()
                this.selProductid="add"
                this.updateProdForm()
                this.message = result.message
                setTimeout(() => this.message = "", 4000)
            }else{
                let result = await response.json()
                this.errorMessage = result.message
                setTimeout(() => this.errorMessage = "", 4000)
            }
        },
        updateProdForm: function () {
            if (this.selProductid === "add") {
                this.selProduct = null
                this.inpName = ""
                this.inpPrice = ""
                this.inpShortDesc = ""
                this.inpDesc = ""
                this.imgPath = "static/src/images/placeholder-image.png"
                this.$refs.inpImage.value=null
                this.file=""
                return
            }
            for (item of this.products) {
                if (item.id == this.selProductid) {
                    this.selProduct = item
                    this.$refs.inpImage.value=null
                    this.file=""
                    break
                }
            }
            this.inpName = this.selProduct.name
            this.inpPrice = this.selProduct.price
            this.inpShortDesc = this.selProduct.shortdesc
            this.inpDesc = this.selProduct.desc
            this.imgPath = this.selProduct.imgpath

        },
        getProducts: async function () {
            const response = await fetch("/products")
            if (response.status === 200) {
                this.products = await response.json()
            }
        }
    },
    computed: {
        admin: function () {
            return (this.user && this.user.role === "admin")
        }
    },
    created: function () {
        this.getProducts()
    }
}