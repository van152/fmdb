char __fastcall sub_140E5CF50(_QWORD *a1, char a2, __int64 a3, int a4, unsigned __int8 a5)
{
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 v11; // rax
  __int64 *v12; // rax
  __int64 v13; // rbx
  unsigned __int64 v14; // rdi
  char v15; // r14
  __int64 v16; // rax
  __int64 *v17; // rax
  __int64 v18; // rax
  __int64 v19; // rax
  __int64 v20; // rcx
  _QWORD *v21; // r14
  _QWORD *v22; // rbx
  _QWORD *v23; // rax
  _QWORD *v24; // rdi
  __int64 v25; // r12
  __int64 *v26; // r12
  __int64 v27; // rdi
  unsigned __int64 v28; // rcx
  __int64 v29; // rbx
  __int64 v30; // rbx
  bool v31; // al
  __int64 v32; // rdi
  bool v33; // al
  __int64 v35; // [rsp+30h] [rbp-10h] BYREF
  char v36; // [rsp+3Eh] [rbp-2h]
  unsigned __int8 v37; // [rsp+3Fh] [rbp-1h]
  __int64 v38; // [rsp+40h] [rbp+0h]

  v38 = -2;
  v36 = a2;
  sub_140F7EC80(a3, (_DWORD)a1 + 216, *(_QWORD *)(a3 + 40), a5, 1, 0);
  sub_140F7EC80(a3, (_DWORD)a1 + 224, *(_QWORD *)(a3 + 40), a5, 1, 0);
  sub_140F7EC80(a3, (_DWORD)a1 + 232, *(_QWORD *)(a3 + 40), a5, 1, 0);
  sub_140F7EC80(a3, (_DWORD)a1 + 240, *(_QWORD *)(a3 + 40), a5, 1, 0);
  sub_140F7EC80(a3, (_DWORD)a1 + 248, *(_QWORD *)(a3 + 8), a5, 1, 0);
  if ( (_BYTE)a4 != 0 )
  {
    sub_140F7FD40(a3, a1 + 40, a5);
    if ( (a5 & 8) != 0 )
    {
      v9 = a1[41];
      if ( v9 != 0 )
        v8 = v9 + *(int *)(*(_QWORD *)(v9 + 8) + 4LL) + 8;
      else
        v8 = 0;
    }
    else
    {
      v8 = a1[41];
    }
    v35 = v8;
    if ( (unsigned __int8)sub_140F80250(a3, &v35, a5, 0) != 0 )
    {
      if ( v35 != 0 )
        v10 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v35 + 1688LL))(v35);
      else
        v10 = 0;
      a1[41] = v10;
    }
    v37 = a4;
    v11 = a1[42];
    if ( v11 != 0 )
      *(_QWORD *)(v11 + 8) = a1;
    v12 = (__int64 *)a1[34];
    if ( v12 == nullptr || (v13 = *v12, v12[1] == *v12) )
    {
      v15 = 0;
    }
    else
    {
      v14 = 0;
      v15 = 0;
      do
      {
        if ( (a5 & 8) != 0 )
        {
          v19 = *(_QWORD *)(v13 + 8 * v14);
          if ( v19 != 0 )
            v18 = v19 + *(int *)(*(_QWORD *)(v19 + 8) + 4LL) + 8;
          else
            v18 = 0;
        }
        else
        {
          v18 = *(_QWORD *)(v13 + 8 * v14);
        }
        v35 = v18;
        if ( (unsigned __int8)sub_140F80250(a3, &v35, a5, 0) != 0 )
        {
          if ( v35 != 0 )
            v16 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v35 + 1688LL))(v35);
          else
            v16 = 0;
          *(_QWORD *)(v13 + 8 * v14) = v16;
          v15 = 1;
        }
        ++v14;
        v17 = (__int64 *)a1[34];
        v13 = *v17;
      }
      while ( v14 < (v17[1] - *v17) >> 3 );
    }
    v20 = a1[42];
    a4 = v37;
    if ( v20 != 0 )
      (*(void (__fastcall **)(__int64, __int64, _QWORD))(*(_QWORD *)v20 + 40LL))(v20, a3, a5);
    if ( v15 != 0 )
    {
      v21 = (_QWORD *)a1[34];
      if ( v21 != nullptr )
      {
        v22 = (_QWORD *)v21[1];
        v23 = (_QWORD *)sub_141751B70(*v21, v22, 0);
        v24 = v23;
        if ( v23 != v22 )
        {
          while ( ++v23 != v22 )
          {
            if ( *v23 != 0 )
              *v24++ = *v23;
          }
        }
        if ( v24 != v22 )
        {
          v25 = v21[1] - (_QWORD)v22;
          sub_141758A00(v24, v22, v25);
          v21[1] = (char *)v24 + v25;
        }
        v26 = (__int64 *)a1[34];
        a4 = v37;
        if ( v26 != nullptr )
        {
          v27 = *v26;
          if ( *v26 == v26[1] )
          {
            if ( v27 != 0 )
            {
              v28 = v26[2] - v27;
              if ( v28 == -1 )
                v28 = *(unsigned int *)(v27 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v29 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v29) >> 3 > v28)
                && (v30 = *(_QWORD *)(v29 + 8 * v28)) != 0 )
              {
                MEMORY[0x1419475D8](v30 + 32, v27 - *(unsigned int *)(v30 + 120));
                v31 = *(_BYTE *)(v30 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v30 + 64)) != 0;
                if ( !v31 && *(_BYTE *)(v30 + 97) != 0 )
                  sub_1412D33C0(v30);
              }
              else
              {
                MEMORY[0x141948990](v27 - *(unsigned int *)(qword_141ABD470 + 48));
              }
              v26[2] = 0;
              v26[1] = 0;
              *v26 = 0;
              a4 = v37;
            }
            if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                               + (unsigned int)TlsIndex)
                                             + 4LL) )
            {
              sub_141750E08(&dword_141B59AA8);
              if ( dword_141B59AA8 == -1 )
              {
                sub_1407E3E70(&unk_141B59A68);
                sub_141751048(sub_1407E4B20);
                sub_141750EA0(&dword_141B59AA8);
                a4 = v37;
              }
            }
            if ( byte_141B59A9C != 0
              && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0xC1
              && (v32 = *(_QWORD *)(qword_141B59A80 + 192)) != 0 )
            {
              MEMORY[0x1419475D8](v32 + 32, (char *)v26 - *(unsigned int *)(v32 + 120));
              v33 = *(_BYTE *)(v32 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) != 0;
              if ( !v33 && *(_BYTE *)(v32 + 97) != 0 )
                sub_1412D33C0(v32);
            }
            else
            {
              MEMORY[0x141948990]((char *)v26 - (unsigned int)dword_141B59A98);
            }
            a1[34] = 0;
          }
        }
      }
    }
  }
  if ( v36 != 0 )
    sub_1411D2F80((_DWORD)a1, 0, a3, a4, a5);
  return 1;
}
