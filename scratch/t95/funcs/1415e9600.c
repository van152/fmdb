// THUNK ALIAS -> sub_144640840 (jmp:0x1415e9600->0x144640840)
__int64 __fastcall sub_144640840(__int64 a1)
{
  __int64 v2; // rsi
  void *v3; // rcx
  _QWORD *v4; // r15
  __int64 *v5; // rbx
  __int64 v6; // r14
  unsigned __int64 v7; // rax
  unsigned __int64 v8; // r12
  unsigned __int64 v9; // rdx
  unsigned __int64 v10; // r12
  __int64 v11; // rdi
  __int64 *v12; // r13
  __int64 v13; // r14
  __int64 v14; // rdi
  unsigned __int64 v15; // rcx
  __int64 v16; // rbx
  __int64 v17; // rbx
  bool v18; // al
  unsigned __int64 v20; // [rsp+48h] [rbp-8h]

  if ( dword_141B5FA18 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                   + 4LL) )
  {
    sub_141750E08(&dword_141B5FA18);
    if ( dword_141B5FA18 == -1 )
    {
      sub_1407E53D0((unsigned int)&unk_141B5F9C8, 1100134596, 500, 136, 0, 1, 500, 4096);
      sub_141751048(sub_140FB4680);
      sub_141750EA0(&dword_141B5FA18);
    }
  }
  v2 = sub_1407E58C0(&unk_141B5F9C8, 136);
  *(_QWORD *)(v2 + 8) = -1;
  *(_DWORD *)(v2 + 16) = 0;
  *(_QWORD *)v2 = 0x141883D28LL;
  v3 = (void *)qword_141ABD470;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    v3 = &unk_141B59A68;
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  *(_QWORD *)(v2 + 96) = 0;
  *(_QWORD *)(v2 + 88) = 0;
  *(_QWORD *)(v2 + 80) = 0;
  *(_QWORD *)(v2 + 72) = 0;
  *(_QWORD *)(v2 + 64) = 0;
  *(_QWORD *)(v2 + 56) = 0;
  *(_QWORD *)(v2 + 48) = 0;
  *(_QWORD *)(v2 + 40) = 0;
  *(_QWORD *)(v2 + 32) = 0;
  *(_QWORD *)(v2 + 24) = 0;
  *(_QWORD *)(v2 + 104) = 124518401;
  *(_DWORD *)(v2 + 112) = 0;
  *(_QWORD *)(v2 + 116) = 0x76C0001076C0001LL;
  *(_WORD *)(v2 + 124) = 0;
  *(_DWORD *)(v2 + 126) = -16384000;
  *(_WORD *)(v2 + 130) = 255;
  *(_BYTE *)(v2 + 132) = 0;
  v4 = *(_QWORD **)a1;
  v5 = *(__int64 **)(*(_QWORD *)a1 + 32LL);
  if ( v5 == *(__int64 **)(*(_QWORD *)a1 + 40LL) )
  {
    v6 = (__int64)v5 - v4[3];
    v7 = v6 >> 3;
    v8 = (unsigned __int64)(v6 >> 3) >> 1;
    v9 = 0x1FFFFFFFFFFFFFFFLL - v8;
    v10 = (v6 >> 3) + v8;
    v20 = (v6 >> 3) + 1;
    if ( v10 <= v20 )
      v10 = v7 + 1;
    if ( v7 > v9 )
      v10 = 0x1FFFFFFFFFFFFFFFLL;
    v11 = sub_1407E4490(v3, 8 * v10);
    *(_QWORD *)(v11 + v6) = v2;
    v12 = (__int64 *)v4[4];
    sub_141758A00();
    if ( v12 != v5 )
      sub_141758A00();
    v13 = v11;
    v14 = v4[3];
    if ( v14 == 0 )
      goto LABEL_23;
    v15 = v4[5] - v14;
    if ( v15 == -1 )
    {
      v15 = *(unsigned int *)(v14 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_22;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_22;
    }
    v16 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v16) >> 3 > v15 )
    {
      v17 = *(_QWORD *)(v16 + 8 * v15);
      if ( v17 != 0 )
      {
        MEMORY[0x1419475D8](v17 + 32, v14 - *(unsigned int *)(v17 + 120));
        v18 = *(_BYTE *)(v17 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17 + 64)) != 0;
        if ( !v18 && *(_BYTE *)(v17 + 97) != 0 )
          sub_1412D33C0(v17);
        goto LABEL_23;
      }
    }
LABEL_22:
    MEMORY[0x141948990](v14 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_23:
    v4[3] = v13;
    v4[4] = v13 + 8 * v20;
    v4[5] = v13 + 8 * v10;
    return v2;
  }
  *v5 = v2;
  v4[4] += 8LL;
  return v2;
}
