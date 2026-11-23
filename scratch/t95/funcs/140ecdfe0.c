// THUNK ALIAS -> sub_143CA4A20 (jmp:0x140ecdfe0->0x143ca4a20)
__int64 __fastcall sub_143CA4A20(__int64 a1, char a2, unsigned int a3, __int64 a4)
{
  __int64 **v5; // rdx
  __int64 *v6; // rax
  __int64 *v7; // rdx
  int v10; // ebp
  int v11; // ecx
  __int64 v12; // rsi
  __int64 v13; // r8

  v5 = *(__int64 ***)(qword_141B60198 + 128);
  v6 = *v5;
  v7 = v5[1];
  if ( v6 == v7 )
    return 0;
  v10 = *(_DWORD *)(a1 + 12);
  v11 = -1;
  if ( a2 == 20 )
    v11 = 22;
  while ( 1 )
  {
    v12 = *v6;
    if ( *(_DWORD *)(*v6 + 76) == v10 && (*(_BYTE *)(v12 + 94) == a2 || v11 == *(char *)(v12 + 94)) )
      break;
    if ( ++v6 == v7 )
    {
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
      v12 = sub_1407E58C0(&unk_141B5E1A8, 96);
      *(_QWORD *)(v12 + 8) = -1;
      *(_DWORD *)(v12 + 16) = 0;
      *(_QWORD *)v12 = 0x14187DF38LL;
      *(_QWORD *)(v12 + 24) = -1;
      *(_QWORD *)(v12 + 32) = -1;
      *(_QWORD *)(v12 + 40) = -1;
      *(_QWORD *)(v12 + 48) = -1;
      *(_QWORD *)(v12 + 56) = 0;
      *(_QWORD *)(v12 + 64) = 0x76C0001076C0001LL;
      *(_DWORD *)(v12 + 72) = 124518401;
      *(_DWORD *)(v12 + 76) = v10;
      *(_QWORD *)(v12 + 80) = -1;
      *(_QWORD *)(v12 + 85) = -1;
      *(_BYTE *)(v12 + 93) = 0;
      *(_BYTE *)(v12 + 94) = a2;
      *(_DWORD *)(v12 + 12) = *(_DWORD *)(qword_141B60198 + 80) + 1;
      LOBYTE(v13) = (_BYTE)word_141B60460 != 6;
      sub_140F6C770(qword_141B60198, v12, v13);
      return sub_141545680(v12, a3, a4);
    }
  }
  return sub_141545680(v12, a3, a4);
}
