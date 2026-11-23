void __fastcall sub_140ED8FD0(__int64 a1, __int64 a2, int a3)
{
  int v4; // ebx
  __int128 v6; // kr00_16
  __int64 v7; // rdi
  _QWORD *v8; // rax
  unsigned __int64 v9; // rcx
  __int64 v10; // rdx
  __int64 v11; // rsi
  _QWORD v12[2]; // [rsp+28h] [rbp-48h] BYREF
  int v13; // [rsp+38h] [rbp-38h] BYREF
  __int64 v14; // [rsp+40h] [rbp-30h] BYREF
  __int128 v15; // [rsp+50h] [rbp-20h] BYREF
  __int64 v16; // [rsp+60h] [rbp-10h]
  __int64 v17; // [rsp+70h] [rbp+0h]

  v17 = -2;
  if ( a2 != 0 )
  {
    v4 = a2;
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
      qword_141ABD470 = (__int64)&unk_141B59A68;
    }
    v15 = 0;
    v16 = 0;
    sub_140ED7E00(v4, (unsigned int)&v15, 0, a3, 0);
    v6 = v15;
    if ( (_QWORD)v15 != *((_QWORD *)&v15 + 1) )
    {
      v7 = v15;
      do
      {
        v8 = *(_QWORD **)(*(_QWORD *)v7 + 24LL);
        if ( v8 != *(_QWORD **)(*(_QWORD *)v7 + 32LL) && *v8 != 0 )
        {
          (*(void (__fastcall **)(_QWORD, int *))(*(_QWORD *)*v8 + 144LL))(*v8, &v13);
          sub_140FEAD00(&v13, v12);
          sub_14083B5F0(a1, v12);
          (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v12[0] + 16LL))(v12[0], v12);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, &v14);
        }
        v7 += 8;
      }
      while ( v7 != *((_QWORD *)&v6 + 1) );
    }
    if ( (_QWORD)v6 != 0 )
    {
      v9 = v16 - v6;
      if ( v16 - (_QWORD)v6 == -1 )
      {
        v9 = *(unsigned int *)(v6 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_21:
          MEMORY[0x141948990](v6 - *(unsigned int *)(qword_141ABD470 + 48));
          return;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_21;
      }
      v10 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v10) >> 3 <= v9 )
        goto LABEL_21;
      v11 = *(_QWORD *)(v10 + 8 * v9);
      if ( v11 == 0 )
        goto LABEL_21;
      MEMORY[0x1419475D8](*((_QWORD *)&v6 + 1) + 32LL, v6 - *(unsigned int *)(*((_QWORD *)&v6 + 1) + 120LL));
      if ( (*(_BYTE *)(*((_QWORD *)&v6 + 1) + 72LL) == 0
         || _InterlockedDecrement((volatile signed __int32 *)(v11 + 64)) == 0)
        && *(_BYTE *)(v11 + 97) != 0 )
      {
        sub_1412D33C0(v11);
      }
    }
  }
}
