__int64 __fastcall sub_141204E80(_QWORD *a1, int a2)
{
  __int64 v4; // rsi
  __int64 v5; // r15
  __int64 v6; // rcx
  _QWORD *v7; // rax
  unsigned __int64 v8; // rdi
  unsigned __int64 v9; // rdx
  unsigned __int64 v10; // r13
  __int64 v11; // r12
  __int64 v12; // rax
  _QWORD *v13; // rcx
  unsigned __int64 v14; // rdi
  __int64 v15; // rbx
  __int64 v16; // rdx
  __int64 v17; // rdi
  unsigned __int64 v18; // rcx
  __int64 v19; // rbx
  bool v20; // al
  unsigned __int64 v21; // rcx
  unsigned __int64 v22; // rdi
  __int64 v23; // rdi
  unsigned __int64 v24; // r13
  volatile signed __int32 *v25; // rbx
  volatile signed __int32 *v26; // rcx
  char v28[8]; // [rsp+48h] [rbp-18h] BYREF
  volatile signed __int32 *v29; // [rsp+50h] [rbp-10h] BYREF
  _QWORD v30[9]; // [rsp+58h] [rbp-8h] BYREF

  v30[1] = -2;
  sub_14080D0E0(a1: v28, a2: 0x1418E2C24LL);
  v30[0] = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)v30,
    a2: (unsigned int)&v29,
    a3: a2,
    a4: (unsigned int)&qword_141B61ED8,
    a5: (__int64)v28,
    a6: 0,
    a7: 0,
    0);
  v4 = (__int64)v29;
  if ( v29 == nullptr )
  {
    LODWORD(v4) = 1;
    if ( qword_141ABF098 != 0 )
      return (unsigned int)v4;
    byte_141ABF0A0 = 1;
    v4 = sub_141750CC0(a1: 32);
    *(_QWORD *)v4 = 0x14188E8D0LL;
    if ( qword_141ABD470 == 0 )
    {
      if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(a1: &dword_141B59AA8);
        if ( dword_141B59AA8 == -1 )
        {
          sub_1407E3E70(a1: &unk_141B59A68);
          sub_141751048(a1: sub_1407E4B20);
          sub_141750EA0(a1: &dword_141B59AA8);
        }
      }
      qword_141ABD470 = (__int64)&unk_141B59A68;
    }
    *(_QWORD *)(v4 + 24) = 0;
    *(_QWORD *)(v4 + 16) = 0;
    *(_QWORD *)(v4 + 8) = 0;
    qword_141ABF098 = v4;
    byte_141ABF0A0 = 0;
    goto LABEL_50;
  }
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v29 + 40LL))(
    a1: v29,
    a2: v30,
    a3: 4);
  if ( *(_DWORD *)(v4 + 16) == 0 )
  {
    v5 = LODWORD(v30[0]);
    v6 = a1[1];
    v7 = (_QWORD *)a1[2];
    v8 = ((__int64)v7 - v6) >> 3;
    if ( v8 > LODWORD(v30[0]) )
    {
      v7 = (_QWORD *)(v6 + 8LL * LODWORD(v30[0]));
LABEL_11:
      a1[2] = v7;
      goto LABEL_42;
    }
    if ( v8 < LODWORD(v30[0]) )
    {
      v9 = (a1[3] - v6) >> 3;
      if ( v9 >= LODWORD(v30[0]) )
      {
        v21 = LODWORD(v30[0]) - v8;
        if ( LODWORD(v30[0]) != v8 )
        {
          v22 = LODWORD(v30[0]) + ~v8;
          if ( (v21 & 3) != 0 )
          {
            v4 = 0;
            do
            {
              *v7++ = 0xFF0F000000000000uLL;
              ++v4;
            }
            while ( (v21 & 3) != v4 );
            v21 -= v4;
          }
          if ( v22 >= 3 )
          {
            do
            {
              *v7 = 0xFF0F000000000000uLL;
              v7[1] = 0xFF0F000000000000uLL;
              v7[2] = 0xFF0F000000000000uLL;
              v7[3] = 0xFF0F000000000000uLL;
              v7 += 4;
              v21 -= 4LL;
            }
            while ( v21 != 0 );
          }
        }
        goto LABEL_11;
      }
      v10 = v9 + (v9 >> 1);
      if ( v10 <= LODWORD(v30[0]) )
        v10 = LODWORD(v30[0]);
      v11 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v10);
      v12 = v5 - v8;
      if ( v5 != v8 )
      {
        v13 = (_QWORD *)(v11 + 8 * v8);
        v14 = v5 + ~v8;
        if ( (v12 & 3) != 0 )
        {
          v15 = 0;
          LODWORD(v4) = 0;
          do
          {
            *v13++ = 0xFF0F000000000000uLL;
            ++v15;
          }
          while ( (v12 & 3) != v15 );
          v12 -= v15;
        }
        if ( v14 >= 3 )
        {
          v16 = 0;
          do
          {
            v13[v16] = 0xFF0F000000000000uLL;
            v13[v16 + 1] = 0xFF0F000000000000uLL;
            v13[v16 + 2] = 0xFF0F000000000000uLL;
            v13[v16 + 3] = 0xFF0F000000000000uLL;
            v16 += 4;
          }
          while ( v12 != v16 );
        }
      }
      sub_141758A00(a1: v11, a2: a1[1], a3: a1[2] - a1[1]);
      v17 = a1[1];
      if ( v17 != 0 )
      {
        v18 = a1[3] - v17;
        if ( v18 == -1 )
          v18 = *(unsigned int *)(v17 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v19 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v19) >> 3 > v18)
          && (v4 = *(_QWORD *)(v19 + 8 * v18)) != 0 )
        {
          MEMORY[0x1419475D8](a1: v4 + 32, a2: v17 - *(unsigned int *)(v4 + 120));
          v20 = *(_BYTE *)(v4 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v4 + 64)) != 0;
          if ( !v20 && *(_BYTE *)(v4 + 97) != 0 )
            sub_1412D33C0(a1: v4);
        }
        else
        {
          MEMORY[0x141948990](a1: v17 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      a1[1] = v11;
      a1[2] = v11 + 8 * v5;
      a1[3] = v11 + 8 * v10;
    }
LABEL_42:
    if ( LODWORD(v30[0]) != 0 )
    {
      v23 = 7;
      v24 = 0;
      do
      {
        v4 = a1[1];
        v25 = v29;
        if ( v29 != nullptr )
          _InterlockedIncrement(v29 + 2);
        (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v25 + 40LL))(
          a1: v25,
          a2: v28,
          a3: 1);
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v25 + 40LL))(
          a1: v25,
          a2: v4 + v23 - 3,
          a3: 1);
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v25 + 40LL))(
          a1: v25,
          a2: v4 + v23 - 2,
          a3: 1);
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v25 + 40LL))(
          a1: v25,
          a2: v4 + v23 - 1,
          a3: 1);
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v25 + 40LL))(
          a1: v25,
          a2: v4 + v23,
          a3: 1);
        LODWORD(v4) = *((_DWORD *)v25 + 4);
        if ( _InterlockedDecrement(v25 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v25)(a1: v25, a2: 1);
        if ( (_DWORD)v4 != 0 )
          goto LABEL_3;
        ++v24;
        v23 += 8;
      }
      while ( v24 < LODWORD(v30[0]) );
    }
LABEL_50:
    LOBYTE(v4) = 1;
    goto LABEL_51;
  }
LABEL_3:
  LODWORD(v4) = 0;
LABEL_51:
  v26 = v29;
  if ( v29 != nullptr && _InterlockedDecrement(v29 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v26)(a1: v26, a2: 1);
  return (unsigned int)v4;
}
