__int64 __fastcall sub_140809170(__int64 *a1, __int64 *a2)
{
  __int64 result; // rax
  volatile signed __int32 *v5; // rcx

  result = *a1;
  if ( *a1 != *a2 )
  {
    v5 = (volatile signed __int32 *)(result - 4);
    if ( result != 0 && _InterlockedDecrement(v5) == 0 )
      sub_1412EC9A0((__int64)v5);
    *a1 = 0;
    result = *a2;
    *a1 = *a2;
    *a2 = 0;
  }
  return result;
}
