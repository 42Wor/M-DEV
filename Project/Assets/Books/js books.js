  <script>

  //phone

  $("#mobile_code").intlTelInput({
          initialCountry: "pk",
          separateDialCode: true
          // utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/11.0.4/js/utils.js"
  });

  // To remove the pre-applied styling
  function remove() {
      let i = 0;
      while (i < 5) {
          stars[i].className = "star";
          i++;
      }
  }

  function handleSelectChange(select) {
    var selectedOption = select.options[select.selectedIndex];
    if (selectedOption.value === 'Chat') {
      enablep('ssmedia','form');
    }
    else if (selectedOption.value === 'Leave Message') {
      enablep('form','ssmedia');
    }
  }

  function enablep(firstId,secondId) {
    var firstElement = document.getElementById(firstId);
    var secondElement = document.getElementById(secondId);

    firstElement.style.display = "block";
   secondElement.style.display = "none";
  }

  </script>
<script>
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.left a').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    const rightContainer = document.querySelector('.right');
                    const offset = targetElement.offsetTop - 200; // Adjust this value as needed
                    rightContainer.scrollTo({
                        top: offset,
                        behavior: 'smooth'
                    });
                }
            });
        });
    });
</script>
