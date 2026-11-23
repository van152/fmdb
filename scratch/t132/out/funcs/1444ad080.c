__int64 __fastcall sub_1444AD080(__int64 a1, __int64 a2)
{
  bool v3; // r8
  __int64 v4; // r9
  unsigned __int64 v5; // rsi
  char v6; // al
  char v7; // cl

  *(_QWORD *)a1 = a2;
  *(_QWORD *)(a1 + 8) = 0x76C0001076C0001LL;
  *(_WORD *)(a1 + 16) = 0;
  *(_DWORD *)(a1 + 18) = 91136;
  *(_BYTE *)(a1 + 22) = 100;
  if ( *(_BYTE *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex) + 8LL) != 0 )
  {
    v3 = false;
  }
  else
  {
    sub_141751038();
    v3 = *(_BYTE *)(a1 + 19) <= 0;
  }
  v4 = *((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex);
  v5 = *(_QWORD *)(v4 + 328);
  *(_QWORD *)(v4 + 328) = *(_QWORD *)(v4 + 336) + 0x5851F42D4C957F2DLL * v5;
  *(_BYTE *)(a1 + 18) = ((int)__ROR4__((v5 >> 27) ^ (v5 >> 45), v5 >> 59) < 0) | 2;
  if ( v3 )
    *(_BYTE *)(a1 + 19) = 100;
  if ( *(char *)(a1 + 20) <= 0 )
    *(_BYTE *)(a1 + 20) = 1;
  v6 = *(_BYTE *)(a1 + 21);
  if ( (unsigned __int8)(v6 - 101) <= 0x9Bu )
  {
    *(_BYTE *)(a1 + 21) = 0;
    v6 = 0;
  }
  v7 = *(_BYTE *)(a1 + 22);
  if ( v7 > 100 || v7 <= v6 )
    *(_BYTE *)(a1 + 22) = 100;
  return a1;
}
