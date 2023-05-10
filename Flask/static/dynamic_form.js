$(document).ready(function() {
    let questionCount = 1;

    // Funktion zum Hinzufügen einer neuen Frage
    function addQuestion() {
        const questionDiv = $('<div>').addClass('form-group');
        const questionLabel = $('<label>').text('Frage ' + questionCount);
        const questionSelect = $('<select>').addClass('form-control question-select');
        questionSelect.append($('<option>').attr('disabled', true).attr('selected', true));
        questionSelect.append($('<option>').text('Frage Typ 1'));
        questionSelect.append($('<option>').text('Frage Typ 2'));
        // Fügen Sie weitere Frage Typen hinzu

        questionDiv.append(questionLabel);
        questionDiv.append(questionSelect);
        $('#questions-container').append(questionDiv);

        questionCount += 1;
    }

    // Event-Handler zum Hinzufügen einer neuen Frage
    $('#add-question-btn').click(function() {
        if (questionCount <= 10) {
            addQuestion();
        } else {
            alert('Sie können nur bis zu 10 Fragen hinzufügen.');
        }
    });

    // Event-Handler zum Ändern des Fragentyps
    $('#questions-container').on('change', '.question-select', function() {
        const selectedType = $(this).val();
        // Logik zum Anzeigen des entsprechenden Frage Typ-Formulars
        // basierend auf dem ausgewählten Typ
    });
});
