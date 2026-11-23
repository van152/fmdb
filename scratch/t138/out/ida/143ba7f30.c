__int64 __fastcall sub_143BA7F30(__int64 a1)
{
  __int64 *v1; // rsi
  __int64 result; // rax

  v1 = *(__int64 **)(a1 + 248);
  result = *v1;
  if ( *v1 == v1[1] )
  {
    result = v1[3];
    if ( result == v1[4]
      && v1[6] == 0
      && v1[7] == 0
      && v1[9] == 0
      && v1[10] == 0
      && v1[11] == 0
      && v1[12] == 0
      && v1[8] == 0 )
    {
      *(_QWORD *)(a1 + 248) = 0;
      sub_14146A230(a1: v1);
      return sub_140E41190(a1: v1);
    }
  }
  return result;
}
