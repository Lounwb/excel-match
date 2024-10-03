<template>
    <img alt="Vue logo" src="../../public/vuetify-logo-v3-slim-light.svg">
    <div class="hello">
        <h1>{{ hi_title }}</h1>
        <div>
            <el-text 
                class="mx-1,text-wrap"
                size="large"
                line-clamp="3">
                We offer online parsing of
            <el-text class="mx-1" type="success" size="large">excel files</el-text>
            to automatically do the matching of data items for you. 
            </el-text>
                <br/>
            <el-text
                class="mx-1,text-line"
                size="large">
                Please upload your 
            <el-text class="mx-1" type="warning" size="large">EXCEL</el-text>
                data file to get the
            <el-text class="mx-1" type="primary" size="large">matching data results.</el-text>
            </el-text>
        </div>
      <div class="container">
        <el-upload
        class="upload-demo"
        ref="upload"
        accept=".xlsx, .xls, .csv"
        drag
        multiple
        :data="form.match_files"
        :show-file-list="true"
        :on-change="(file, fileList) => {handleChange(file, fileList, 'match')}"
        :on-remove="(file, fileList) => {handleRemove(file, fileList, 'match')}"
        :auto-upload="false"
        style="width: 35%;"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            Drop file here or <em>click to upload</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              Please upload the <el-text tag="b">Match</el-text> files here
            </div>
          </template>
        </el-upload>
          <el-upload
          class="upload-demo"
          ref="upload"
          accept=".xlsx, .xls, .csv"
          drag
          multiple
          :data="form.candidate_files"
          :show-file-list="true"
          :on-change="(file, fileList) => {handleChange(file, fileList, 'candidate')}"
          :on-remove="(file, fileList) => {handleRemove(file, fileList, 'candidate')}"
          :auto-upload="false"
          style="width: 35%; margin-left: 50px;"
          >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            Drop file here or <em>click to upload</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              Please upload the <el-text tag="b">Candidate</el-text> files here
            </div>
          </template>
        </el-upload>
      </div>
      <el-form 
        :model="form" 
        :rules="form_rules"
        ref="formRef"
        label-width="auto"
        style="max-width: 600px; margin-left: 30%; margin-top: 20px;">
        <el-form-item label="Joined file name" prop="file_name">
          <el-input v-model="form.file_name" />
        </el-form-item>
        <el-form-item label="Output file type">
          <el-select v-model="form.type" placeholder="please select file type">
            <el-option label="xlsx" value="xlsx" />
            <el-option label="csv" value="csv" />
            <el-option label="xls" value="xls" />
          </el-select>
        </el-form-item>
        <el-form-item label="Join mode">
          <el-radio-group v-model="form.mode">
            <el-radio value="left">Left join</el-radio>
            <el-radio value="right">Right join</el-radio>
            <el-radio value="inner">Inner join</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Match attribute name" prop="match">
          <el-input v-model="form.match" />
        </el-form-item>
        <el-form-item label="Candidate attribute name" prop="candidate">
          <el-input v-model="form.candidate" />
        </el-form-item>
      </el-form>

      <el-button 
        class="upload-submit-button"
        slot="trigger" 
        size="large" 
        type="primary" 
        :disabled="isDisabled"
        @click="submitUpload">
        {{ buttonText }}
      </el-button>
    </div>
    <el-divider style="max-width: 50%; margin: 0 auto; margin-top: 100px;"/>
    <Footer></Footer>
  </template>
  
  <script>
  import { UploadFilled } from '@element-plus/icons-vue'
  import { ElButton, FormInstance, FormRules, ElMessage, ElMessageBox, ElNotification } from 'element-plus';
  import { ref } from 'vue';
  import api from "@/api/request.js"
  import router from '@/router';
  import Footer from '@/components/Footer.vue';

  
  export default {
    name: 'mainVue',
    components: { UploadFilled, ElButton, Footer },
    created() {
      document.title = 'Match Excels | Upload and Analysis';
      this.messageAlert()
    },
    data() {
      return {
        match_ref: ref(),
        candidate_ref: ref(),
        form_valid: false,
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        hi_title: "Upload Your EXCEL Files for A Quick Start",
        isDisabled: false,
        buttonText: 'Upload and Download',
        showProgress: true,
        uploadProgress: 0,
        form: {
          'file_name': '',
          'match': '',
          'candidate': '',
          'mode': 'inner',
          'type': 'xlsx',
          'match_files': [],
          'candidate_files': []
        },
        form_rules: {
          file_name: [
            { 
              required: true, 
              message: 'Please input File name',
              trigger: 'blur'  
            },
            {
              min: 2,
              max: 10,
              message: '2 to 16 characters in length',
              trigger: 'blur'
            }
          ],
          match: [
            {
              required: true,
              message: 'Please input Match attribute name',
              trigger: 'blur' 
            }
          ],
          candidate: [
            {
              required: true,
              message: 'Please input Candidate attribute name',
              trigger: 'blur' 
            }
          ]
        }
      };
    },
    methods: {
      handleChange (file, fileList, type) {
        if(type == 'match'){
          this.form.match_files = fileList
        } else {
          this.form.candidate_files = fileList
        }
      },
      handleRemove (file, fileList, type) {
        if (type == 'match') {
          this.form.match_files = fileList
        } else {
          this.form.candidate_files = fileList
        }
      },
      submitUpload() {
        if (this.form.match_files.length === 0) {
          ElNotification({
            title: 'Warning',
            message: 'Please upload your match EXCEL files first!',
            type: 'warning'
          })
        } else if (this.form.candidate_files.length === 0) {
          ElNotification({
            title: 'Warning',
            message: 'Please upload your candidate EXCEL files first!',
            type: 'warning'
          }) 
        } else {
          // verify match files is xlsx, xls or csv
          for (let i = 0; i < this.form.match_files.length; i++){
            let match_file = this.form.match_files[i]
            var appendix = match_file.name.substring(match_file.name.lastIndexOf('.') + 1)
            const suffix = (appendix === 'xlsx' || appendix === 'xls' || appendix === 'csv') 
            if (!suffix) {
              ElNotification({
                  title: 'Warning',
                  message: appendix.toUpperCase() + " file type is not supported! Please upload EXCEL files.",
                  type: 'warning'
                })
              return false
            }
          }
          for (let i = 0; i < this.form.candidate_files.length; i++){
            let match_file = this.form.candidate_files[i]
            var appendix = match_file.name.substring(match_file.name.lastIndexOf('.') + 1)
            const suffix = (appendix === 'xlsx' || appendix === 'xls' || appendix === 'csv') 
            if (!suffix) {
              ElNotification({
                  title: 'Warning',
                  message: appendix.toUpperCase() + " file type is not supported! Please upload EXCEL files.",
                  type: 'warning'
                })
              return false
            }
          }
          this.$refs.formRef.validate(valid => {
            if (valid) {
              var form_data = new FormData()
                
              for (let i = 0; i < this.form.match_files.length; i++) {
                form_data.append("match_files", this.form.match_files[i].raw, this.form.match_files[i].name)
              }
              for (let i = 0; i < this.form.candidate_files.length; i++) {
                form_data.append("candidate_files", this.form.candidate_files[i].raw, this.form.candidate_files[i].name)
              }
              let merge_condition = {
                'match': this.form.match,
                'condition': 'equal',
                'candidate': this.form.candidate
              }
              form_data.append("merge_condition", JSON.stringify(merge_condition))
              form_data.append("mode", this.form.mode)
              form_data.append("file_name", this.form.file_name + '.' + this.form.type)

              const response = api({
                url: "/match",
                method: "post",
                data: form_data,
                headers: this.headers,
                onUploadProgress: (progressEvent_1) => {
                  this.uploadProgress = Math.round(
                    (progressEvent_1.loaded * 100) / progressEvent_1.total
                  );
                }
              }).then((response) => {
                let loc = response.data.message;

                window.open('/api/download?location=' + loc, '_blank');
                ElNotification({
                  title: 'Success',
                  message: 'The match is complete and downloading.',
                  type: 'success'
                });
              }).catch((e) => {
                let response_1 = e.response;
                let msg = response_1.data.message;

                ElNotification({
                  title: 'Error',
                  message: msg,
                  type: 'error'
                });
              })
            }
          });
        }
      },
      messageAlert() {
        ElMessageBox.alert(' \
        1. Make sure your files are all the same file type. \
        </br>2. Make sure your excel files all meet the first row as the table header and the second row starts with the data. \
        </br>3. Make sure your file does not contain hidden rows and merged cells. \
        </br>4. Make sure your file does not have duplicate listings.', 'Instructions', {
          confirmButtonText: 'OK',
          type: 'warning',
          roundButton: true,
          center: true,
          dangerouslyUseHTMLString: true,
          draggable: true,
          callback: (action) => {

          }
        })
      }
    }
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  h3 {
    margin: 40px 0 0;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
  .upload-demo {
    width: 50%;
  }
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    margin-top: 20px;
  }
  .upload-submit-button {
    margin-top: 20px;
    size: 10px;
  }
  .progress {
    width: 50%;
    margin: 0 auto;
    margin-top: 20px;
  }
  .text-wrap {
    margin-bottom: 20px;
  }
  .text-line {
    margin-top: 20px;
  }
  .el-menu--horizontal > .el-menu-item:nth-child(1) {
    margin-right: auto;
  }
  </style>
  