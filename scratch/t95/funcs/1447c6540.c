__int64 __fastcall sub_1447C6540(__int64 a1)
{
  int v2; // eax
  __int64 v3; // rdx

  if ( (_QWORD)xmmword_141AC5D80 == -1 )
    v2 = sub_141758B80();
  else
    v2 = sub_141758BE0(&xmmword_141AC5D80, a1);
  v3 = 0;
  if ( v2 == 0 )
    return a1;
  return v3;
}
