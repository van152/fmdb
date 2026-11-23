void __fastcall sub_140FAF5B0(__int64 a1, __int64 a2, __int64 a3, char a4)
{
  __int64 **v7; // rax
  __int64 *v8; // rbx
  __int64 *v9; // rsi
  __int64 v10; // rax
  __int64 v11; // rcx
  volatile signed __int32 *v12; // rsi
  volatile signed __int32 *v13; // rsi
  __int64 v14; // rsi
  int v15; // edi
  __int64 v16; // rcx
  _QWORD *v17; // rax
  volatile signed __int32 *v18; // rbx
  int v19; // r8d
  __int64 v20; // r12
  int v21; // eax
  char v22; // bl
  void (__fastcall ***v23)(_QWORD, __int64); // rcx
  _QWORD *v24; // rax
  __int64 v25; // r13
  __int64 v26; // rbx
  __int64 v27; // rdx
  unsigned __int64 v28; // rax
  __int64 *v29; // rax
  __int64 *v30; // rdx
  __int64 *v31; // rcx
  __int64 *v32; // rsi
  __int64 v33; // rcx
  __int64 v34; // rax
  __int64 v35; // r8
  __int64 v36; // rsi
  unsigned __int64 v37; // rcx
  __int64 v38; // r8
  __int64 v39; // r13
  bool v40; // al
  __int64 v41; // rsi
  unsigned __int64 v42; // rcx
  __int64 v43; // rbx
  __int64 v44; // rbx
  bool v45; // al
  _QWORD *v46; // r14
  __int64 v47; // rdi
  __int64 *v48; // r15
  unsigned __int64 v49; // rcx
  _QWORD *v50; // rsi
  __int64 v51; // rbx
  __int64 v52; // rbx
  bool v53; // al
  __int64 v54; // rsi
  unsigned __int64 v55; // rcx
  __int64 v56; // rbx
  __int64 v57; // rdi
  bool v58; // al
  char v59; // si
  volatile signed __int32 *v60; // rcx
  __int64 v61; // rcx
  void (__fastcall ***v62)(_QWORD, __int64); // rcx
  _QWORD *v63; // rdi
  _QWORD *v64; // rbx
  _QWORD *v65; // rsi
  int v66; // [rsp+30h] [rbp-50h]
  __int64 v67; // [rsp+40h] [rbp-40h] BYREF
  unsigned __int64 v68; // [rsp+48h] [rbp-38h]
  _QWORD *v69; // [rsp+50h] [rbp-30h]
  _QWORD *v70; // [rsp+58h] [rbp-28h]
  _QWORD *v71; // [rsp+60h] [rbp-20h]
  __int64 v72; // [rsp+68h] [rbp-18h] BYREF
  unsigned int v73; // [rsp+70h] [rbp-10h] BYREF
  __int64 v74; // [rsp+78h] [rbp-8h] BYREF
  volatile signed __int32 *v75; // [rsp+80h] [rbp+0h] BYREF
  char v76; // [rsp+8Fh] [rbp+Fh] BYREF
  __int64 v77; // [rsp+90h] [rbp+10h] BYREF
  char v78; // [rsp+9Fh] [rbp+1Fh] BYREF
  __int64 v79; // [rsp+A0h] [rbp+20h]

  v79 = -2;
  if ( (_BYTE)a3 != 0 )
  {
    v7 = *(__int64 ***)(a1 + 128);
    v8 = *v7;
    v9 = v7[1];
    if ( *v7 != v9 )
    {
      while ( 1 )
      {
        v10 = *v8;
        LOBYTE(v74) = 0;
        v77 = v10;
        v11 = *(_QWORD *)(a2 + 56);
        if ( v11 == 0 )
          break;
        (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v11 + 16LL))(a1: v11, a2: &v77, a3: &v74);
        if ( ++v8 == v9 )
          goto LABEL_5;
      }
LABEL_137:
      sub_141758410();
      goto LABEL_138;
    }
  }
LABEL_5:
  if ( *(_BYTE *)(a1 + 89) != 0 || a4 == 0 )
    return;
  v67 = 0;
  LOBYTE(a3) = 1;
  sub_140F45A00(a1: &qword_141B5FDA8, a2: &v74, a3, a4: &v67);
  if ( v74 != 0 )
  {
    v72 = 0;
    sub_14080D0E0(a1: &v73, a2: 0x1418E2C24LL);
    sub_140FFADB0(a1, a2: &v72, a3: 0, a4: 0);
    v77 = 0x80100004E554C4CLL;
    sub_1407D0F70(
      a1: (unsigned int)&v77,
      a2: (unsigned int)&v75,
      a3: (unsigned int)&v74,
      a4: (unsigned int)&v72,
      a5: (__int64)&v73,
      a6: 0,
      a7: 0,
      0);
    v12 = v75;
    if ( v75 != nullptr )
    {
      (*(void (__fastcall **)(volatile signed __int32 *, unsigned int *, __int64))(*(_QWORD *)v75 + 40LL))(
        a1: v75,
        a2: &v73,
        a3: 4);
      if ( *((_DWORD *)v12 + 4) != 0 )
        goto LABEL_107;
      v13 = v75;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v75 + 40LL))(
        a1: v75,
        a2: a1 + 92,
        a3: 1);
      if ( *((_DWORD *)v13 + 4) != 0 )
        goto LABEL_107;
      if ( dword_141B5F498 <= *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                        + 4LL) )
      {
LABEL_12:
        v14 = sub_1407E58C0(a1: &unk_141B5F448, a2: 88);
        *(_QWORD *)(v14 + 8) = -1;
        *(_DWORD *)(v14 + 16) = 0;
        *(_QWORD *)v14 = 0x1418837A8LL;
        *(_QWORD *)(v14 + 24) = 0;
        *(_QWORD *)(v14 + 32) = -1;
        if ( qword_141ABD470 == 0 )
          qword_141ABD470 = sub_1407E4940();
        v71 = (_QWORD *)(v14 + 40);
        *(_QWORD *)(v14 + 80) = 0;
        *(_QWORD *)(v14 + 72) = 0;
        *(_QWORD *)(v14 + 64) = 0;
        *(_QWORD *)(v14 + 56) = 0;
        *(_QWORD *)(v14 + 48) = 0;
        v70 = (_QWORD *)v14;
        *(_QWORD *)(v14 + 40) = 0;
        if ( v73 != 0 )
        {
          v15 = 0;
          while ( 1 )
          {
            v18 = v75;
            (*(void (__fastcall **)(volatile signed __int32 *, char *, __int64))(*(_QWORD *)v75 + 40LL))(
              a1: v75,
              a2: &v76,
              a3: 1);
            if ( *((_DWORD *)v18 + 4) != 0 )
              goto LABEL_86;
            if ( dword_141B5F498 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                               + (unsigned int)TlsIndex)
                                             + 4LL) )
            {
              sub_141750E08(a1: &dword_141B5F498);
              if ( dword_141B5F498 == -1 )
              {
                sub_1407E53D0(
                  a1: (unsigned int)&unk_141B5F448,
                  a2: 1100129062,
                  a3: 100,
                  a4: 88,
                  a5: 0,
                  a6: 1,
                  a7: 100,
                  a8: 4096);
                sub_141751048(a1: sub_140FB4430);
                sub_141750EA0(a1: &dword_141B5F498);
              }
            }
            v20 = sub_1407E58C0(a1: &unk_141B5F448, a2: 88);
            *(_QWORD *)(v20 + 8) = -1;
            *(_DWORD *)(v20 + 16) = 0;
            *(_QWORD *)v20 = 0x1418837A8LL;
            *(_QWORD *)(v20 + 24) = 0;
            *(_QWORD *)(v20 + 32) = -1;
            if ( qword_141ABD470 == 0 )
            {
              if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                                 + (unsigned int)TlsIndex)
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
            *(_QWORD *)(v20 + 80) = 0;
            *(_QWORD *)(v20 + 72) = 0;
            *(_QWORD *)(v20 + 64) = 0;
            *(_QWORD *)(v20 + 56) = 0;
            *(_QWORD *)(v20 + 48) = 0;
            *(_QWORD *)(v20 + 40) = 0;
            v21 = *(_DWORD *)(a1 + 84);
            v77 = (__int64)v75;
            if ( v75 != nullptr )
              _InterlockedIncrement(v75 + 2);
            LOBYTE(v66) = 1;
            LOBYTE(v19) = 1;
            v22 = sub_141566B00(
                    a1: v20,
                    a2: (unsigned int)&v77,
                    a3: v19,
                    a4: (unsigned int)&qword_141B5FDA8,
                    a5: v21,
                    a6: v15,
                    a7: v66,
                    a8: 0);
            v23 = (void (__fastcall ***)(_QWORD, __int64))v77;
            if ( v77 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v77 + 8)) == 0 )
              (**v23)(a1: v23, a2: 1);
            v24 = (_QWORD *)(v20 + 40);
            if ( v22 == 0 )
            {
              if ( *(_QWORD *)(v20 + 64) != 0 )
              {
                sub_1407E4890(a1: qword_141ABD470);
                v24 = (_QWORD *)(v20 + 40);
                *(_QWORD *)(v20 + 80) = 0;
                *(_QWORD *)(v20 + 72) = 0;
                *(_QWORD *)(v20 + 64) = 0;
              }
              v63 = v70;
              v64 = v71;
              if ( *v24 != 0 )
              {
                v65 = v24;
                sub_1407E4890(a1: qword_141ABD470);
                v65[2] = 0;
                v65[1] = 0;
                *v65 = 0;
              }
              sub_140FB00C0(a1: v20);
              if ( v63[8] != 0 )
              {
                sub_1407E4890(a1: qword_141ABD470);
                v63[10] = 0;
                v63[9] = 0;
                v63[8] = 0;
              }
              if ( *v64 != 0 )
              {
                sub_1407E4890(a1: qword_141ABD470);
                v64[2] = 0;
                v64[1] = 0;
                *v64 = 0;
              }
              sub_140FB00C0(a1: v63);
              v59 = 0;
              goto LABEL_108;
            }
            v69 = (_QWORD *)(v20 + 40);
            v25 = qword_141B5FE40;
            if ( *(_BYTE *)(qword_141B5FE40 + 89) != 0 )
              break;
LABEL_52:
            v78 = 0;
            v77 = v20;
            v33 = *(_QWORD *)(a2 + 56);
            if ( v33 == 0 )
              goto LABEL_137;
            (*(void (__fastcall **)(__int64, __int64 *, char *))(*(_QWORD *)v33 + 16LL))(a1: v33, a2: &v77, a3: &v78);
            if ( v78 != 0 )
            {
              v34 = sub_141758910(a1: v20, a2: 0, a3: &unk_141A7F570, a4: &unk_141AAF9E0, a5: 0);
              if ( v34 != 0 )
              {
                LOBYTE(v35) = 1;
                sub_140F6C770(a1, a2: v34, a3: v35);
              }
            }
            else
            {
              v36 = *(_QWORD *)(v20 + 64);
              if ( v36 != 0 )
              {
                v37 = *(_QWORD *)(v20 + 80) - v36;
                if ( v37 == -1 )
                  v37 = *(unsigned int *)(v36 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v38 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v38) >> 3 > v37)
                  && (v39 = *(_QWORD *)(v38 + 8 * v37)) != 0 )
                {
                  MEMORY[0x1419475D8](a1: v39 + 32, a2: v36 - *(unsigned int *)(v39 + 120));
                  v40 = *(_BYTE *)(v39 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v39 + 64)) != 0;
                  if ( !v40 && *(_BYTE *)(v39 + 97) != 0 )
                    sub_1412D33C0(a1: v39);
                }
                else
                {
                  MEMORY[0x141948990](a1: v36 - *(unsigned int *)(qword_141ABD470 + 48));
                }
                *(_QWORD *)(v20 + 80) = 0;
                *(_QWORD *)(v20 + 72) = 0;
                *(_QWORD *)(v20 + 64) = 0;
              }
              v41 = *v69;
              if ( *v69 != 0 )
              {
                v42 = *(_QWORD *)(v20 + 56) - v41;
                if ( v42 == -1 )
                  v42 = *(unsigned int *)(v41 - *(unsigned int *)(qword_141ABD470 + 48));
                if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                  && (v43 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v43) >> 3 > v42)
                  && (v44 = *(_QWORD *)(v43 + 8 * v42)) != 0 )
                {
                  MEMORY[0x1419475D8](a1: v44 + 32, a2: v41 - *(unsigned int *)(v44 + 120));
                  v45 = *(_BYTE *)(v44 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v44 + 64)) != 0;
                  if ( !v45 && *(_BYTE *)(v44 + 97) != 0 )
                    sub_1412D33C0(a1: v44);
                }
                else
                {
                  MEMORY[0x141948990](a1: v41 - *(unsigned int *)(qword_141ABD470 + 48));
                }
                v17 = v69;
                v69[2] = 0;
                v17[1] = 0;
                *v17 = 0;
              }
              sub_140FB00C0(a1: v20);
            }
            if ( ++v15 >= v73 )
              goto LABEL_86;
          }
          if ( **(_QWORD **)(qword_141B5FE40 + 128) != *(_QWORD *)(*(_QWORD *)(qword_141B5FE40 + 128) + 8LL) )
          {
            v26 = *(_QWORD *)(v20 + 24);
            v27 = 0;
            if ( (int)v26 < 0 )
            {
LABEL_51:
              *(_QWORD *)(v20 + 24) = v27;
              goto LABEL_52;
            }
            if ( *(_QWORD *)(qword_141B5FE40 + 40) == 0 )
            {
              v68 = (unsigned int)v26;
              v28 = (*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)qword_141B5FE40 + 48LL))(
                      a1: qword_141B5FE40,
                      a2: 0);
              if ( v28 > v68 )
                goto LABEL_49;
            }
            v29 = *(__int64 **)(v25 + 32);
            v30 = (__int64 *)v29[1];
            v31 = v29;
            if ( *((_BYTE *)v30 + 25) == 0 )
            {
              v31 = *(__int64 **)(v25 + 32);
              do
              {
                v32 = v30 + 2;
                if ( *((_DWORD *)v30 + 7) >= (int)v26 )
                {
                  v31 = v30;
                  v32 = v30;
                }
                v30 = (__int64 *)*v32;
              }
              while ( *(_BYTE *)(*v32 + 25) == 0 );
            }
            if ( *((_BYTE *)v31 + 25) != 0 )
            {
              v27 = 0;
              goto LABEL_51;
            }
            if ( *((_DWORD *)v31 + 7) <= (int)v26 )
            {
              v27 = 0;
              if ( v31 == v29 )
                goto LABEL_51;
              LODWORD(v26) = *((_DWORD *)v31 + 8);
              if ( (int)v26 >= 0 )
              {
LABEL_49:
                v27 = *(_QWORD *)(**(_QWORD **)(v25 + 128) + 8LL * (unsigned int)v26);
                goto LABEL_51;
              }
            }
          }
          v27 = 0;
          goto LABEL_51;
        }
LABEL_86:
        v46 = v70;
        v47 = v70[8];
        v48 = v71;
        if ( v47 != 0 )
        {
          v49 = v70[10] - v47;
          if ( v49 == -1 )
            v49 = *(unsigned int *)(v47 - *(unsigned int *)(qword_141ABD470 + 48));
          v50 = v70 + 8;
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v51 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v51) >> 3 > v49)
            && (v52 = *(_QWORD *)(v51 + 8 * v49)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v52 + 32, a2: v47 - *(unsigned int *)(v52 + 120));
            v53 = *(_BYTE *)(v52 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v52 + 64)) != 0;
            if ( !v53 && *(_BYTE *)(v52 + 97) != 0 )
              sub_1412D33C0(a1: v52);
          }
          else
          {
            MEMORY[0x141948990](a1: v47 - *(unsigned int *)(qword_141ABD470 + 48));
          }
          v46[10] = 0;
          v46[9] = 0;
          *v50 = 0;
        }
        v54 = *v48;
        if ( *v48 != 0 )
        {
          v55 = v46[7] - v54;
          if ( v55 == -1 )
            v55 = *(unsigned int *)(v54 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v56 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v56) >> 3 > v55)
            && (v57 = *(_QWORD *)(v56 + 8 * v55)) != 0 )
          {
            MEMORY[0x1419475D8](a1: v57 + 32, a2: v54 - *(unsigned int *)(v57 + 120));
            v58 = *(_BYTE *)(v57 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v57 + 64)) != 0;
            if ( !v58 && *(_BYTE *)(v57 + 97) != 0 )
              sub_1412D33C0(a1: v57);
          }
          else
          {
            MEMORY[0x141948990](a1: v54 - *(unsigned int *)(qword_141ABD470 + 48));
          }
          v48[2] = 0;
          v48[1] = 0;
          *v48 = 0;
        }
        sub_140FB00C0(a1: v46);
LABEL_107:
        v59 = 1;
LABEL_108:
        v60 = v75;
        if ( v75 != nullptr && _InterlockedDecrement(v75 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v60)(a1: v60, a2: 1);
        v61 = v72;
        if ( v72 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v72 - 4)) == 0 )
          sub_1412EC9A0(a1: v61 - 4);
        if ( v59 == 0 )
          goto LABEL_116;
        goto LABEL_115;
      }
LABEL_138:
      sub_141750E08(a1: &dword_141B5F498);
      if ( dword_141B5F498 == -1 )
      {
        sub_1407E53D0(
          a1: (unsigned int)&unk_141B5F448,
          a2: 1100129062,
          a3: 100,
          a4: 88,
          a5: 0,
          a6: 1,
          a7: 100,
          a8: 4096);
        sub_141751048(a1: sub_140FB4430);
        sub_141750EA0(a1: &dword_141B5F498);
      }
      goto LABEL_12;
    }
    v16 = v72;
    if ( v72 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v72 - 4)) == 0 )
      sub_1412EC9A0(a1: v16 - 4);
  }
LABEL_115:
  LOWORD(qword_141B60330) = 3569;
LABEL_116:
  v62 = (void (__fastcall ***)(_QWORD, __int64))v74;
  if ( v74 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v74 + 8)) == 0 )
    (**v62)(a1: v62, a2: 1);
}
