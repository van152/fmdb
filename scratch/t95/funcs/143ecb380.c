__int64 __fastcall sub_143ECB380(__int64 a1)
{
  __int64 result; // rax
  __int64 v3; // rdi
  __int64 v4; // rdx
  __int64 v5; // rsi
  int v6; // ecx

  sub_1410522B0(
    *(_QWORD *)(a1 + 96),
    *(_QWORD *)(a1 + 104),
    0xAAAAAAAAAAAAAAABuLL * ((__int64)(*(_QWORD *)(a1 + 104) - *(_QWORD *)(a1 + 96)) >> 3));
  result = *(_QWORD *)(a1 + 96);
  v3 = *(_QWORD *)(a1 + 104);
  if ( (int)(-1431655765 * ((unsigned __int64)(v3 - result) >> 3)) >= 2 )
  {
    v4 = 45;
    v5 = 0;
    do
    {
      ++v5;
      if ( *(_BYTE *)(result + v4 - 3) == *(_BYTE *)(result + v4 - 27)
        && *(_BYTE *)(result + v4) == *(_BYTE *)(result + v4 - 24)
        && *(_BYTE *)(result + v4 - 2) == *(_BYTE *)(result + v4 - 26)
        && *(_WORD *)(result + v4 - 29) == *(_WORD *)(result + v4 - 5)
        && *(float *)(result + v4 - 21) > *(float *)(result + v4 - 45) )
      {
        v6 = *(_DWORD *)(result + v4 - 17);
        if ( *(_DWORD *)(result + v4 - 37) > v6 )
        {
          *(_DWORD *)(result + v4 - 37) = v6;
          result = *(_QWORD *)(a1 + 96);
          v3 = *(_QWORD *)(a1 + 104);
        }
      }
      v4 += 24;
    }
    while ( v5 < (int)(-1431655765 * ((unsigned __int64)(v3 - result) >> 3) - 1) );
  }
  return result;
}
