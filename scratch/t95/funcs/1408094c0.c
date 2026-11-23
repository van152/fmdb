__int64 *__fastcall sub_1408094C0(__int64 *a1, __int64 *a2, __int64 a3)
{
  __int64 v3; // rax

  *a2 = 0;
  if ( a2 != a1 )
  {
    v3 = *a1;
    if ( *a1 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v3 - 4));
    *a2 = v3;
  }
  sub_140809710(a2, a3, 0xFFFFFFFFLL);
  return a2;
}
