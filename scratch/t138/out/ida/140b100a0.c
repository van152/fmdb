__int64 __fastcall sub_140B100A0(_QWORD *a1, int a2)
{
  __int64 *v4; // rdi
  volatile signed __int32 *v5; // rsi
  __int64 v6; // r15
  __int64 v7; // rbx
  volatile signed __int32 *v8; // rbp
  int v9; // esi
  bool v10; // si
  __int64 v11; // rsi
  unsigned __int64 v12; // rax
  unsigned __int64 v13; // r14
  unsigned __int64 v14; // r13
  unsigned __int64 v15; // rcx
  unsigned __int64 v16; // r13
  __int64 v17; // rbp
  __int64 *v18; // rbx
  unsigned __int64 v19; // rcx
  __int64 v20; // rbx
  __int64 v21; // rsi
  volatile signed __int32 *v22; // rsi
  __int64 v23; // r13
  __int64 *v24; // rbp
  __int64 v25; // rsi
  __int64 v26; // rsi
  __int64 v27; // rax
  __int64 v28; // rsi
  __int64 v29; // r8
  __int64 v30; // rsi
  int v31; // edi
  void (__fastcall ***v32)(_QWORD, __int64); // rcx
  int v33; // esi
  __int64 v34; // rsi
  unsigned __int64 v35; // rax
  unsigned __int64 v36; // rbx
  unsigned __int64 v37; // r15
  unsigned __int64 v38; // rcx
  unsigned __int64 v39; // r15
  __int64 v40; // r14
  __int64 *v41; // rbp
  unsigned __int64 v42; // rcx
  __int64 v43; // rbp
  __int64 v44; // rsi
  bool v45; // al
  __int64 *v46; // rcx
  void (__fastcall ***v47)(_QWORD, __int64); // rcx
  __int64 v48; // rsi
  volatile signed __int32 *v49; // rcx
  volatile signed __int32 *v51; // rsi
  _QWORD *v52; // r12
  int v53; // r14d
  volatile signed __int32 *v54; // rsi
  volatile signed __int32 *v55; // rsi
  volatile signed __int32 *v56; // rsi
  volatile signed __int32 *v57; // rsi
  __int16 v58; // si
  __int16 v59; // [rsp+48h] [rbp-80h] BYREF
  char v60[2]; // [rsp+4Ah] [rbp-7Eh] BYREF
  __int16 v61[4]; // [rsp+4Ch] [rbp-7Ch] BYREF
  unsigned int v62; // [rsp+54h] [rbp-74h] BYREF
  volatile signed __int32 *v63; // [rsp+58h] [rbp-70h] BYREF
  __int16 v64; // [rsp+66h] [rbp-62h] BYREF
  _QWORD v65[2]; // [rsp+68h] [rbp-60h] BYREF
  int v66; // [rsp+7Ch] [rbp-4Ch] BYREF
  __int64 v67; // [rsp+80h] [rbp-48h] BYREF

  v67 = 0x80100004E554C4CLL;
  v4 = v65;
  sub_14080D0E0(a1: v65, a2: 0x1418E2C24LL);
  sub_1407D0F70(
    a1: (unsigned int)&v67,
    a2: (unsigned int)&v63,
    a3: a2,
    a4: (unsigned int)&qword_141B5B720,
    a5: (__int64)v65,
    a6: 0,
    a7: 0,
    0);
  v5 = v63;
  if ( v63 == nullptr )
  {
    LOBYTE(v4) = 1;
    return (unsigned int)v4;
  }
  (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v63 + 40LL))(
    a1: v63,
    a2: &v62,
    a3: 4);
  if ( *((_DWORD *)v5 + 4) == 0 )
  {
    if ( v62 != 0 )
    {
      v6 = 0;
      while ( 1 )
      {
        v7 = sub_141750CC0(a1: 12);
        *(_QWORD *)v7 = -4170448895LL;
        *(_DWORD *)(v7 + 8) = 0xFFFFFF;
        v8 = v63;
        if ( v63 != nullptr )
          _InterlockedIncrement(v63 + 2);
        LOBYTE(v65[0]) = 0;
        (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v8 + 40LL))(
          a1: v8,
          a2: v65,
          a3: 1);
        if ( *((_DWORD *)v8 + 4) != 0 )
          break;
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(
          a1: v8,
          a2: v7 + 4,
          a3: 4);
        if ( *((_DWORD *)v8 + 4) != 0 )
          break;
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(
          a1: v8,
          a2: v7 + 10,
          a3: 1);
        if ( *((_DWORD *)v8 + 4) != 0 )
          break;
        _InterlockedIncrement(v8 + 2);
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(
          a1: v8,
          a2: v7,
          a3: 4);
        v9 = *((_DWORD *)v8 + 4);
        if ( _InterlockedDecrement(v8 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v8)(a1: v8, a2: 1);
        if ( v9 != 0 )
          break;
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(
          a1: v8,
          a2: v7 + 11,
          a3: 1);
        if ( *((_DWORD *)v8 + 4) != 0 )
          break;
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(
          a1: v8,
          a2: v7 + 8,
          a3: 2);
        v10 = *((_DWORD *)v8 + 4) == 0;
        if ( _InterlockedDecrement(v8 + 2) == 0 )
          goto LABEL_17;
LABEL_18:
        if ( !v10 )
        {
          v46 = (__int64 *)v7;
          goto LABEL_97;
        }
        v4 = (__int64 *)a1[5];
        if ( v4 == (__int64 *)a1[6] )
        {
          v11 = (__int64)v4 - a1[4];
          v12 = v11 >> 3;
          v13 = (v11 >> 3) + 1;
          v14 = (unsigned __int64)(v11 >> 3) >> 1;
          v15 = 0x1FFFFFFFFFFFFFFFLL - v14;
          v16 = (v11 >> 3) + v14;
          if ( v16 <= v13 )
            v16 = v12 + 1;
          if ( v12 > v15 )
            v16 = 0x1FFFFFFFFFFFFFFFLL;
          v17 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v16);
          *(_QWORD *)(v17 + v11) = v7;
          v18 = (__int64 *)a1[5];
          sub_141758A00(a1: v17, a2: a1[4], a3: (char *)v4 - a1[4]);
          if ( v18 != v4 )
            sub_141758A00(a1: v17 + v11 + 8, a2: v4, a3: a1[5] - (_QWORD)v4);
          v4 = (__int64 *)a1[4];
          if ( v4 != nullptr )
          {
            v19 = a1[6] - (_QWORD)v4;
            if ( v19 == -1 )
            {
              v19 = *(unsigned int *)((char *)v4 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                goto LABEL_36;
            }
            else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            {
              goto LABEL_36;
            }
            v20 = *(_QWORD *)(qword_141ABD470 + 24);
            if ( (*(_QWORD *)(qword_141ABD470 + 32) - v20) >> 3 > v19 && (v21 = *(_QWORD *)(v20 + 8 * v19)) != 0 )
            {
              v4 = (__int64 *)((char *)v4 - *(unsigned int *)(v21 + 120));
              MEMORY[0x1419475D8](a1: v21 + 32, a2: v4);
              if ( (*(_BYTE *)(v21 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v21 + 64)) == 0)
                && *(_BYTE *)(v21 + 97) != 0 )
              {
                sub_1412D33C0(a1: v21);
              }
            }
            else
            {
LABEL_36:
              v4 = (__int64 *)((char *)v4 - *(unsigned int *)(qword_141ABD470 + 48));
              MEMORY[0x141948990](a1: v4);
            }
          }
          a1[4] = v17;
          a1[5] = v17 + 8 * v13;
          a1[6] = v17 + 8 * v16;
          goto LABEL_6;
        }
        *v4 = v7;
        a1[5] += 8LL;
LABEL_6:
        if ( ++v6 >= (unsigned __int64)v62 )
          goto LABEL_43;
      }
      v10 = false;
      if ( _InterlockedDecrement(v8 + 2) != 0 )
        goto LABEL_18;
LABEL_17:
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v8)(a1: v8, a2: 1);
      goto LABEL_18;
    }
LABEL_43:
    v22 = v63;
    (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v63 + 40LL))(
      a1: v63,
      a2: &v62,
      a3: 4);
    if ( *((_DWORD *)v22 + 4) == 0 )
    {
      if ( v62 != 0 )
      {
        v23 = 0;
        while ( 1 )
        {
          v24 = (__int64 *)sub_141750CC0(a1: 24);
          *v24 = 0;
          v24[1] = 0;
          v24[2] = 0x76C0001FFFFFFFFLL;
          v65[0] = v63;
          _InterlockedIncrement(v63 + 2);
          v25 = v65[0];
          LOBYTE(v59) = 0;
          (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)v65[0] + 40LL))(a1: v65[0], a2: &v59, a3: 1);
          if ( *(_DWORD *)(v25 + 16) != 0 )
            break;
          v26 = *v24;
          if ( *v24 != 0 )
          {
            if ( *(_QWORD *)(v26 + 8) != 0 )
              sub_140B52770();
            sub_140B11330(a1: v26);
          }
          if ( dword_141B5B780 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(a1: &dword_141B5B780);
            if ( dword_141B5B780 == -1 )
            {
              sub_1407E53D0(
                a1: (unsigned int)&unk_141B5B730,
                a2: 1100141344,
                a3: 64,
                a4: 32,
                a5: 0,
                a6: 0,
                a7: 64,
                a8: 4096);
              sub_141751048(a1: sub_140B18F10);
              sub_141750EA0(a1: &dword_141B5B780);
            }
          }
          v27 = sub_1407E58C0(a1: &unk_141B5B730, a2: 32);
          *(_DWORD *)v27 = -1;
          *(_WORD *)(v27 + 4) = 2815;
          *(_QWORD *)(v27 + 16) = -4170448895LL;
          *(_DWORD *)(v27 + 24) = -1;
          *(_WORD *)(v27 + 28) = -1;
          *(_QWORD *)(v27 + 8) = 0;
          *v24 = v27;
          v28 = v65[0];
          (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v65[0] + 40LL))(
            a1: v65[0],
            a2: v24 + 2,
            a3: 4);
          if ( *(_DWORD *)(v28 + 16) != 0 )
            break;
          if ( (unsigned __int8)sub_1413C62C0(a1: *v24, a2: v65) == 0 )
            break;
          LOBYTE(v29) = 4 - (byte_141B5FC2C == 0);
          if ( (unsigned __int8)sub_140F80980(a1: v24 + 1, a2: v65, a3: v29) == 0 )
            break;
          v30 = v65[0];
          if ( v65[0] != 0 )
          {
            _InterlockedIncrement((volatile signed __int32 *)(v65[0] + 8LL));
            (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v30 + 40LL))(
              a1: v30,
              a2: (__int64)v24 + 20,
              a3: 4);
          }
          v31 = *(_DWORD *)(v30 + 16);
          if ( _InterlockedDecrement((volatile signed __int32 *)(v30 + 8)) == 0 )
            (**(void (__fastcall ***)(__int64, __int64))v30)(a1: v30, a2: 1);
          if ( v31 != 0 )
            break;
          v32 = (void (__fastcall ***)(_QWORD, __int64))v65[0];
          v33 = *(_DWORD *)(v65[0] + 16LL);
          if ( _InterlockedDecrement((volatile signed __int32 *)(v65[0] + 8LL)) == 0 )
            (**v32)(a1: v32, a2: 1);
          if ( v33 != 0 )
            goto LABEL_92;
          v4 = (__int64 *)a1[8];
          if ( v4 == (__int64 *)a1[9] )
          {
            v34 = (__int64)v4 - a1[7];
            v35 = v34 >> 3;
            v36 = (v34 >> 3) + 1;
            v37 = (unsigned __int64)(v34 >> 3) >> 1;
            v38 = 0x1FFFFFFFFFFFFFFFLL - v37;
            v39 = (v34 >> 3) + v37;
            if ( v39 <= v36 )
              v39 = v35 + 1;
            if ( v35 > v38 )
              v39 = 0x1FFFFFFFFFFFFFFFLL;
            v40 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v39);
            *(_QWORD *)(v40 + v34) = v24;
            v41 = (__int64 *)a1[8];
            sub_141758A00(a1: v40, a2: a1[7], a3: (char *)v4 - a1[7]);
            if ( v41 != v4 )
              sub_141758A00(a1: v40 + v34 + 8, a2: v4, a3: a1[8] - (_QWORD)v4);
            v4 = (__int64 *)a1[7];
            if ( v4 != nullptr )
            {
              v42 = a1[9] - (_QWORD)v4;
              if ( v42 == -1 )
                v42 = *(unsigned int *)((char *)v4 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v43 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v43) >> 3 > v42)
                && (v44 = *(_QWORD *)(v43 + 8 * v42)) != 0 )
              {
                v4 = (__int64 *)((char *)v4 - *(unsigned int *)(v44 + 120));
                MEMORY[0x1419475D8](a1: v44 + 32, a2: v4);
                v45 = *(_BYTE *)(v44 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v44 + 64)) != 0;
                if ( !v45 && *(_BYTE *)(v44 + 97) != 0 )
                  sub_1412D33C0(a1: v44);
              }
              else
              {
                v4 = (__int64 *)((char *)v4 - *(unsigned int *)(qword_141ABD470 + 48));
                MEMORY[0x141948990](a1: v4);
              }
            }
            a1[7] = v40;
            a1[8] = v40 + 8 * v36;
            a1[9] = v40 + 8 * v39;
          }
          else
          {
            *v4 = (__int64)v24;
            a1[8] += 8LL;
          }
          if ( ++v23 >= (unsigned __int64)v62 )
            goto LABEL_103;
        }
        v47 = (void (__fastcall ***)(_QWORD, __int64))v65[0];
        if ( v65[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v65[0] + 8LL)) == 0 )
          (**v47)(a1: v47, a2: 1);
LABEL_92:
        v48 = *v24;
        if ( *v24 != 0 )
        {
          if ( *(_QWORD *)(v48 + 8) != 0 )
            sub_140B52770();
          sub_140B11330(a1: v48);
        }
        v46 = v24;
LABEL_97:
        sub_141750CFC(a1: v46);
      }
      else
      {
LABEL_103:
        LOBYTE(v4) = 1;
        if ( WORD2(v67) < 3u )
          goto LABEL_99;
        v51 = v63;
        (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v63 + 40LL))(
          a1: v63,
          a2: &v66,
          a3: 4);
        if ( *((_DWORD *)v51 + 4) == 0 )
        {
          if ( v66 <= 0 )
            goto LABEL_99;
          v52 = a1 + 10;
          v53 = 0;
          while ( 1 )
          {
            v59 = 0;
            v60[0] = 0;
            v61[0] = 0;
            v54 = v63;
            (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)v63 + 40LL))(
              a1: v63,
              a2: v61,
              a3: 2);
            if ( *((_DWORD *)v54 + 4) != 0 )
              break;
            if ( WORD2(v67) < 4u )
            {
              v60[0] = 0;
            }
            else
            {
              v55 = v63;
              (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v63 + 40LL))(
                a1: v63,
                a2: v60,
                a3: 1);
              if ( *((_DWORD *)v55 + 4) != 0 )
                break;
            }
            v56 = v63;
            (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)v63 + 40LL))(
              a1: v63,
              a2: &v59,
              a3: 2);
            if ( *((_DWORD *)v56 + 4) != 0 )
              break;
            v57 = v63;
            (*(void (__fastcall **)(volatile signed __int32 *, __int16 *, __int64))(*(_QWORD *)v63 + 40LL))(
              a1: v63,
              a2: &v64,
              a3: 2);
            if ( *((_DWORD *)v57 + 4) != 0 )
              break;
            v58 = v64;
            sub_140B18F20(a1: v52, a2: v65, a3: &v59);
            *(_WORD *)(v65[0] + 32LL) = v58;
            if ( ++v53 >= v66 )
              goto LABEL_99;
          }
        }
      }
    }
  }
  LODWORD(v4) = 0;
LABEL_99:
  v49 = v63;
  if ( v63 != nullptr && _InterlockedDecrement(v63 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v49)(a1: v49, a2: 1);
  return (unsigned int)v4;
}
