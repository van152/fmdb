__int64 __fastcall sub_144026550(__int64 a1, char a2, unsigned int a3, __int64 a4)
{
  int v7; // ebp
  __int64 **v8; // rcx
  __int64 *v9; // rax
  __int64 *v10; // rcx
  __int64 v11; // rsi
  __int64 v12; // r8

  v7 = *(_DWORD *)(a1 + 12);
  v8 = *(__int64 ***)(qword_141B60190 + 128);
  v9 = *v8;
  v10 = v8[1];
  while ( v9 != v10 )
  {
    v11 = *v9;
    if ( *(_DWORD *)(*v9 + 76) == v7 && *(_BYTE *)(v11 + 94) == a2 )
      return sub_141545680(v11, a3, a4);
    ++v9;
  }
  if ( dword_141B5E1F8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B5E1F8);
    if ( dword_141B5E1F8 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5E1A8, 1100155733, 10000, 96, 0, 1, 10000, 4096);
      sub_141751048(sub_140ED17F0);
      sub_141750EA0(&dword_141B5E1F8);
    }
  }
  v11 = sub_1407E58C0(&unk_141B5E1A8, 96);
  *(_QWORD *)(v11 + 8) = -1;
  *(_DWORD *)(v11 + 16) = 0;
  *(_QWORD *)v11 = 0x14187DF38LL;
  *(_QWORD *)(v11 + 24) = -1;
  *(_QWORD *)(v11 + 32) = -1;
  *(_QWORD *)(v11 + 40) = -1;
  *(_QWORD *)(v11 + 48) = -1;
  *(_QWORD *)(v11 + 56) = 0;
  *(_QWORD *)(v11 + 64) = 0x76C0001076C0001LL;
  *(_DWORD *)(v11 + 72) = 124518401;
  *(_DWORD *)(v11 + 76) = v7;
  *(_QWORD *)(v11 + 80) = -1;
  *(_QWORD *)(v11 + 85) = -1;
  *(_BYTE *)(v11 + 93) = 0;
  *(_BYTE *)(v11 + 94) = a2;
  *(_DWORD *)(v11 + 12) = *(_DWORD *)(qword_141B60190 + 80) + 1;
  LOBYTE(v12) = (_BYTE)word_141B60460 != 6;
  sub_140F6C770(qword_141B60190, v11, v12);
  return sub_141545680(v11, a3, a4);
}
