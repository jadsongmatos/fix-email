function LevenshteinDistance(s1, s2: string): Integer;
var
  i, j, custo, tamanho1, tamanho2: Integer;
  matriz: array of array of Integer;
begin
  tamanho1 := Length(s1);
  tamanho2 := Length(s2);
  
  SetLength(matriz, tamanho1 + 1, tamanho2 + 1);

  for i := 0 to n do matriz[i,0] := i;
  for j := 0 to m do matriz[0,j] := j;
  
  for i := 1 to tamanho1 do
    for j := 1 to tamanho2 do
    begin
      if s1[i] = s2[j] then
        custo := 0
      else
        custo := 1;
      
      matriz[i, j] := Min(Min(matriz[i-1, j] + 1, matriz[i, j-1] + 1), matriz[i-1, j-1] + custo);
    end;
  
  Result := matriz[tamanho1, tamanho2];
end;


uses
  System.RegularExpressions;

function CorrectEmail(const InputEmail: string; var ValidEmail: Boolean): string;
var
  Email, CorrectedEmail: string;
begin
  // Initial corrections here, using StringReplace, TRegEx, etc.
  Email := Trim(InputEmail);

  // Example: Correct double @ symbols
  Email := TRegEx.Replace(Email, '@+', '@');

  // Set result and validity
  CorrectedEmail := Email; // Apply further corrections as needed
  ValidEmail := TRegEx.IsMatch(CorrectedEmail, {RFC5322 regex pattern here});

  Result := CorrectedEmail;
end;

uses
  System.SysUtils, System.RegularExpressions, System.StrUtils, System.Classes;

function CorrectEmail(emailInput: string; var TLDs: TStringList): string;
var
  email, novoEmail, tldCorreto, parte: string;
  i, posicaoTLD: Integer;
  emailParts, emailTLDParts: TStringList;
  match: TMatch;
  regex: TRegEx;
  distancias: TStringList;
begin
  // Define a expressão regular conforme o RFC 5322
  regex.Create('([A-Za-z0-9-!#$%&''*+/=?^_`{|}~]+(?:\.[A-Za-z0-9-!#$%&''*+/=?^_`{|}~]+)*)@((?:[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\.)*[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)');

  // Remover espaços e caracteres especiais
  email := StringReplace(emailInput, ' ', '', [rfReplaceAll]);
  email := StringReplace(email, ':', '', [rfReplaceAll]);
  email := StringReplace(email, ';', '', [rfReplaceAll]);
  email := StringReplace(email, '<', '', [rfReplaceAll]);
  email := StringReplace(email, '>', '', [rfReplaceAll]);
  email := StringReplace(email, '[', '', [rfReplaceAll]);
  email := StringReplace(email, ']', '', [rfReplaceAll]);
  email := StringReplace(email, '\', '', [rfReplaceAll]);
  email := StringReplace(email, ',', '.', [rfReplaceAll]);

  // Corrigir '@@' e '..'
  email := TRegEx.Replace(email, '@+', '@');
  email := TRegEx.Replace(email, '\.+', '@');

  if StartsStr('.', email) then
    Delete(email, 1, 1);
  if EndsStr('.', email) then
    SetLength(email, Length(email) - 1);

  email := UpperCase(email);
  for i := 0 to TLDs.Count - 1 do
  begin
    if EndsStr(UpperCase(TLDs[i]), email) then
    begin
      posicaoTLD := Length(email) - Length(TLDs[i]);
      if email[posicaoTLD - 1] = '_' then
        email := Copy(email, 1, posicaoTLD - 2) + '.' + Copy(email, posicaoTLD, MaxInt);
    end;
  end;

  email := StringReplace(email, '@@', '@', [rfReplaceAll]);

  // Divide o e-mail e corrige se houver múltiplos '@'
  emailParts := TStringList.Create;
  try
    ExtractStrings(['@'], [], PChar(emailInput), emailParts);
    if emailParts.Count > 2 then
    begin
      for i := 0 to emailParts.Count - 1 do
      begin
        novoEmail := emailParts[i - 1] + '@' + StringReplace(emailParts[i], '@', '', [rfReplaceAll]);
        if regex.IsMatch(novoEmail) then
          email := novoEmail;
      end;
    end;
  finally
    emailParts.Free;
  end;

  emailTLDParts := TStringList.Create;
  try
    ExtractStrings(['.'], [], PChar(email), emailTLDParts);
    if emailTLDParts.Count > 1 then
    begin
      tldCorreto := emailTLDParts[emailTLDParts.Count - 1].ToUpper;
      if TLDs.IndexOf(tldCorreto) = -1 then
      begin
        // Aqui você precisaria implementar uma função para calcular a distância de Levenshtein
        // e encontrar o TLD mais próximo. Isso é mais complexo em Delphi e requer uma implementação
        // adicional que não é trivial de se fazer em um exemplo curto.
      end;
    end;
  finally
    emailTLDParts.Free;
  end;

  match := regex.Match(email);
  if match.Success then
    Result := email
  else
    Result := '';
end;