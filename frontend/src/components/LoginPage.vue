<script>
export default {
  data(){
    return{
      formData{
        email: "",
        password: ""
      }
    }
  }
  methods:{
    loginUser(event){
      event.preventDefault()
      console.log(`Username: ${this.formData.username}, Password: ${this.formData.password}`)
    }
  }
}
</script>

<template>
    <div id="main">
            <div id="canvas" class="overflow-auto">
                <div id="form-body">
                    <h1>Welcome to Vehicle Parking</h1>
                    <h2>Login Form</h2>
                    <form @submit="loginUser">
                        <div class="mb-3">
                            <label for="Input1"
                                class="form-label">Registered Email ID</label>
                            <input type="text" class="form-control"
                                id="Input1"
                                placeholder="Enter email id" v-model="formData.email">
                        </div>
                        <div class="mb-3">
                            <label for="Input2"
                                class="form-label">Password</label>
                            <input type="password" class="form-control"
                                id="Input2"
                                placeholder="Enter password" v-model="formData.password">
                        </div>
                        <div style="text-align: center;">
                            <input type="submit"
                                class="btn btn-primary" value="Login"><br>
                            Are you a new user? <a href="/register">Register</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
</template>

<style>
#canvas {
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  padding: 40px;
  min-width: 600px;
  height: 550px;
}

#form-body {
  text-align: center;
  height: 450px;
  margin-top: 10px;
}

h1 {
  color: #333;
  margin-bottom: 10px;
  font-size: 28px;
}

h2 {
  color: #666;
  margin-bottom: 30px;
  font-size: 20px;
}

.form-control {
  margin-bottom: 15px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 100%;
}

.btn-primary {
  background: #007bff;
  border: none;
  padding: 12px 30px;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  margin-bottom: 15px;
}

.btn-primary:hover {
  background: #0056b3;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
