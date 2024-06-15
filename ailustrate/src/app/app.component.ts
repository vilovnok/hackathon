import { Component } from '@angular/core';
import { FormBuilder, FormControl } from '@angular/forms';
import { DataService } from './data.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'AIllustrate';

  text: string = '';
  title_img: string = 'ночной город';
  image = 'assets/night_city.png';
  
  base64Image: string = '';
  isLoading: boolean = false;
  selection = { value: 'default' }

  textControl = new FormControl('');



  constructor(
    private service: DataService,
    private fb: FormBuilder) { }

  sendPrompt() {
    let formData = this.fb.group({ text: this.textControl.value });
    if (this.textControl.value) {
      this.isLoading = true;
      this.service.handle_post_requests(formData.value, 'generate/prompt-prepoccesing').subscribe(res => {
        if (res['type'] == 'image') {
          this.image=`data:image/jpeg;base64,`+ res['image_bytes'];
          this.title_img=res['title'];                  
        } else if(res['type'] == 'text'){
          this.text=res['text']
        }
        this.isLoading = false;
      }, (err) => {
        this.isLoading = false;
        if (err.status == 422) {
          console.log("BAD 422");
        }
      });
      this.textControl.setValue('');
    } else {
      console.log("я не отправил");
    }
  }

  onImageError(event: Event) {
    const element = event.target as HTMLImageElement;
    element.style.display = 'none';
  }
}
