__int64 *__fastcall sub_140FE77A0(__int64 a1, __int64 *a2)
{
  int v2; // eax
  int v3; // ecx
  int v5[2]; // [rsp+20h] [rbp-8h] BYREF

  if ( a1 != 0 )
  {
    v2 = *(_DWORD *)(a1 + 12);
    v3 = *(_DWORD *)(a1 + 16);
    if ( v3 == 0 )
      v3 = v2;
  }
  else
  {
    v2 = -1;
    v3 = -1;
  }
  v5[0] = v2;
  v5[1] = v3;
  return sub_140FE72B0(v5, 1937006948, a2);
}
