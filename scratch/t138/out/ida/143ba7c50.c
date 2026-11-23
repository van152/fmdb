__int64 __fastcall sub_143BA7C50(__int64 *a1, __int64 *a2)
{
  __int64 result; // rax
  __int64 v3; // rsi

  if ( a1 != a2 )
  {
    result = *a2;
    *a2 = 0;
    v3 = *a1;
    *a1 = result;
    if ( v3 != 0 )
    {
      sub_14146A230(a1: v3);
      return sub_140E41190(a1: v3);
    }
  }
  return result;
}
