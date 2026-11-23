__int64 __fastcall sub_140035F10(__int64 a1, int a2, char a3, char a4)
{
  volatile signed __int32 *v6; // rbx
  __int64 v7; // rax
  unsigned __int64 v8; // r15
  __int64 v9; // rsi
  __int64 v10; // r12
  __int64 v11; // rax
  __int64 v12; // rax
  int v13; // r8d
  int v14; // r9d
  volatile signed __int32 *v15; // rdi
  _QWORD *v16; // rax
  __int64 v17; // rax
  __int64 v18; // rax
  __int64 v19; // rax
  char v20; // al
  bool v21; // cl
  _QWORD *v22; // rax
  __int64 v23; // rbx
  __int64 v24; // rdi
  __int64 v25; // rax
  __int64 v26; // rax
  __int64 v27; // rdi
  volatile signed __int32 *v28; // rcx
  _QWORD *v29; // rax
  __int64 v30; // rbx
  __int64 v31; // rdi
  volatile signed __int32 *v32; // rdi
  volatile signed __int32 *v33; // rcx
  _QWORD *v34; // rax
  __int64 v35; // rbx
  __int64 v36; // rdi
  volatile signed __int32 *v37; // rcx
  _QWORD *v38; // rax
  volatile signed __int32 *v39; // rcx
  __int64 v40; // rbx
  __int64 v41; // rdi
  volatile signed __int32 *v42; // rdi
  int v43; // r12d
  char v44; // bl
  _QWORD *v45; // rax
  _QWORD *v46; // rax
  _QWORD *v47; // rax
  __int64 v48; // rdi
  __int64 v49; // rbx
  __int64 v50; // rdi
  __int64 v51; // rdi
  void (__fastcall ***v52)(_QWORD, __int64); // rcx
  void *v53; // rdi
  __int64 v54; // rax
  __int64 v55; // r8
  __int64 v56; // rax
  __int64 v57; // rax
  void (__fastcall ***v58)(_QWORD, __int64); // rcx
  _QWORD *v59; // rax
  _QWORD *v60; // rax
  __int64 v61; // rdi
  __int64 v62; // rcx
  __int64 v63; // rdx
  volatile signed __int32 *v64; // rcx
  _QWORD *v65; // rax
  __int64 v66; // rsi
  __int64 v67; // rbx
  __int64 v68; // rax
  __int64 v69; // rax
  int v71; // [rsp+20h] [rbp-108h]
  volatile signed __int32 *v72; // [rsp+40h] [rbp-E8h] BYREF
  __int64 v73; // [rsp+48h] [rbp-E0h] BYREF
  int v74; // [rsp+50h] [rbp-D8h]
  __int64 v75; // [rsp+58h] [rbp-D0h] BYREF
  volatile signed __int32 *v76; // [rsp+60h] [rbp-C8h] BYREF
  __int64 v77; // [rsp+68h] [rbp-C0h]
  char v78[8]; // [rsp+70h] [rbp-B8h] BYREF
  char v79[8]; // [rsp+78h] [rbp-B0h] BYREF
  int v80; // [rsp+80h] [rbp-A8h]
  char v81; // [rsp+84h] [rbp-A4h]
  char v82; // [rsp+85h] [rbp-A3h]
  char v83; // [rsp+86h] [rbp-A2h]
  char v84; // [rsp+87h] [rbp-A1h]
  int v85; // [rsp+88h] [rbp-A0h]
  char v86[8]; // [rsp+90h] [rbp-98h] BYREF
  volatile signed __int32 *v87; // [rsp+98h] [rbp-90h] BYREF
  char v88[8]; // [rsp+A0h] [rbp-88h] BYREF
  char v89[8]; // [rsp+A8h] [rbp-80h] BYREF
  __int64 v90; // [rsp+B0h] [rbp-78h] BYREF
  __int64 v91; // [rsp+B8h] [rbp-70h]
  char v92[8]; // [rsp+C8h] [rbp-60h] BYREF
  _BYTE v93[88]; // [rsp+D0h] [rbp-58h] BYREF

  LODWORD(v6) = a2;
  v77 = a1;
  sub_1407C9510(a1: &v90);
  sub_140310A50(a1: v78);
  sub_140310A50(a1: v79);
  v80 = 124518401;
  v81 = (char)v6;
  v82 = a3;
  v84 = a4;
  v83 = 1;
  v85 = 16777473;
  BYTE2(v85) = sub_140F644B0();
  sub_140F4BFB0(a1: &v90, a2: v78);
  v7 = v90;
  if ( v91 == v90 )
  {
LABEL_166:
    v43 = 2;
    goto LABEL_177;
  }
  v8 = 0;
  v9 = v77;
  while ( 1 )
  {
    v10 = sub_14083E160(a1: *(_QWORD *)(v7 + 8 * v8));
    v11 = sub_140835850(a1: v10, a2: 1986359923);
    sub_14083E100(a1: v11, a2: v89);
    v12 = sub_140835850(a1: v10, a2: 1718185061);
    sub_14083E100(a1: v12, a2: v88);
    sub_1407C2920(a1: v93, a2: v89);
    v6 = *(volatile signed __int32 **)(v9 + 45328);
    v15 = *(volatile signed __int32 **)(v9 + 45336);
    if ( v15 != v6 )
    {
      while ( 1 )
      {
        v73 = sub_140809850(a1: v88);
        v74 = sub_140310DB0(a1: v88);
        if ( (unsigned __int8)sub_14080B890(a1: v6, a2: &v73) != 0 )
          break;
        v6 += 2;
        if ( v6 == v15 )
        {
          v6 = v15;
          break;
        }
      }
      if ( v6 == *(volatile signed __int32 **)(v9 + 45336)
        || (v6 = (volatile signed __int32 *)(((unsigned __int64)v6 - *(_QWORD *)(v9 + 45328)) & 0x7FFFFFFF8LL)) == (volatile signed __int32 *)0x7FFFFFFF8LL )
      {
        sub_140808B00(a1: v88);
        sub_140808B00(a1: v89);
        goto LABEL_4;
      }
    }
    if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
    {
      v16 = &unk_141ABD978;
      while ( 1 )
      {
        v16 = (_QWORD *)v16[2];
        if ( v16 == nullptr || *v16 == 0 )
          break;
        if ( (*((_BYTE *)v16 + 28) & 1) == 0 || *((int *)v16 + 6) > 1 )
          goto LABEL_22;
      }
      v6 = (volatile signed __int32 *)sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: (_DWORD)v6, a2: 1099914335, a3: 11101, a4: 1100015773, a5: 0, a6: 1);
      v17 = sub_1407E0010(a1: v6, a2: 0x14193FF91LL);
      v18 = sub_1407D6070(a1: v17, a2: v88);
      v19 = sub_1407E0010(a1: v18, a2: 0x141942145LL);
      sub_1407D6070(a1: v19, a2: v89);
      if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v6) & 4) != 0 )
        sub_1407CD750();
    }
LABEL_22:
    LOBYTE(v13) = 1;
    LOBYTE(v14) = 1;
    v20 = sub_14000F6D0(a1: v9, a2: v10, a3: v13, a4: v14, a5: 0, a6: 1, a7: 0);
    v21 = (dword_141ABD994 & 1) == 0 || dword_141ABD990 >= 2;
    if ( v20 == 0 )
      break;
    if ( !v21 )
    {
      v22 = &unk_141ABD978;
      while ( 1 )
      {
        v22 = (_QWORD *)v22[2];
        if ( v22 == nullptr || *v22 == 0 )
          break;
        if ( (*((_BYTE *)v22 + 28) & 1) == 0 || *((int *)v22 + 6) > 1 )
          goto LABEL_32;
      }
      v23 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v23, a2: 1099914335, a3: 11110, a4: 1100015773, a5: 0, a6: 1);
      v24 = sub_1407E0010(a1: v23, a2: 0x1419414E4LL);
      v25 = sub_140835850(a1: v10, a2: 1851878757);
      sub_14083E100(a1: v25, a2: &v73);
      v26 = sub_1407D6070(a1: v24, a2: &v73);
      v27 = sub_1407E0010(a1: v26, a2: 0x141942406LL);
      sub_1407C31B0(a1: v93, a2: &v72, a3: 0);
      sub_1407D6070(a1: v27, a2: &v72);
      v9 = v77;
      sub_140808B00(a1: &v72);
      sub_140808B00(a1: &v73);
      if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v23) & 4) != 0 )
        sub_1407CD750();
    }
LABEL_32:
    sub_1407D5DC0(a1: qword_141ABD878, a2: &v72, a3: &qword_141B5EDF0);
    v76 = nullptr;
    if ( v72 == nullptr )
      goto LABEL_113;
    v87 = v72;
    _InterlockedIncrement(v72 + 2);
    sub_140F57E80(a1: &qword_141B5FDA8, a2: &v73, a3: &v87);
    v28 = v72;
    if ( v72 == (volatile signed __int32 *)v73 )
    {
      if ( v72 != nullptr && _InterlockedDecrement(v72 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v28)(a1: v28, a2: 1);
    }
    else
    {
      if ( v72 != nullptr && _InterlockedDecrement(v72 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v28)(a1: v28, a2: 1);
      v72 = (volatile signed __int32 *)v73;
    }
    if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
    {
      v29 = &unk_141ABD978;
      while ( 1 )
      {
        v29 = (_QWORD *)v29[2];
        if ( v29 == nullptr || *v29 == 0 )
          break;
        if ( (*((_BYTE *)v29 + 28) & 1) == 0 || *((int *)v29 + 6) > 1 )
          goto LABEL_51;
      }
      v30 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v30, a2: 1099914335, a3: 11120, a4: 1100015773, a5: 0, a6: 1);
      v31 = sub_1407E0010(a1: v30, a2: 0x141940216LL);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v72 + 32LL))(a1: v72, a2: &v73);
      sub_1407D6070(a1: v31, a2: &v73);
      sub_140808B00(a1: &v73);
      if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v30) & 4) != 0 )
        sub_1407CD750();
    }
LABEL_51:
    v32 = v72;
    sub_1407D8AB0(a1: &v73, a2: 0x14191EB1BLL);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64 *, __int64 *, volatile signed __int32 **, int))(*(_QWORD *)v32 + 216LL))(
      a1: v32,
      a2: &v75,
      a3: &qword_141B59758,
      a4: &v73,
      a5: &v76,
      a6: 1);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v72 + 120LL))(a1: v72, a2: &v73);
    v33 = v72;
    if ( v72 == (volatile signed __int32 *)v73 )
    {
      if ( v72 != nullptr && _InterlockedDecrement(v72 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v33)(a1: v33, a2: 1);
      if ( v72 == nullptr )
        goto LABEL_88;
    }
    else
    {
      if ( v72 != nullptr && _InterlockedDecrement(v72 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v33)(a1: v33, a2: 1);
      v72 = (volatile signed __int32 *)v73;
      if ( v73 == 0 )
        goto LABEL_88;
    }
    if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
    {
      v34 = &unk_141ABD978;
      while ( 1 )
      {
        v34 = (_QWORD *)v34[2];
        if ( v34 == nullptr || *v34 == 0 )
          break;
        if ( (*((_BYTE *)v34 + 28) & 1) == 0 || *((int *)v34 + 6) > 1 )
          goto LABEL_71;
      }
      v35 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v35, a2: 1099914335, a3: 11125, a4: 1100015773, a5: 0, a6: 1);
      v36 = sub_1407E0010(a1: v35, a2: 0x14194031FLL);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v72 + 32LL))(a1: v72, a2: &v73);
      sub_1407D6070(a1: v36, a2: &v73);
      sub_140808B00(a1: &v73);
      if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v35) & 4) != 0 )
        sub_1407CD750();
    }
LABEL_71:
    sub_1407D2400(a1: v72, a2: &v73, a3: &qword_141B5E408);
    v37 = v72;
    if ( v72 == (volatile signed __int32 *)v73 )
    {
      if ( v72 != nullptr && _InterlockedDecrement(v72 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v37)(a1: v37, a2: 1);
      if ( v72 != nullptr )
      {
LABEL_76:
        if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
        {
          v38 = &unk_141ABD978;
          while ( 1 )
          {
            v38 = (_QWORD *)v38[2];
            if ( v38 == nullptr || *v38 == 0 )
              break;
            if ( (*((_BYTE *)v38 + 28) & 1) == 0 || *((int *)v38 + 6) > 1 )
              goto LABEL_92;
          }
          v40 = sub_1407E2C90(a1: 2160);
          sub_1407E2EB0(a1: v40, a2: 1099914335, a3: 11129, a4: 1100015773, a5: 0, a6: 1);
          v41 = sub_1407E0010(a1: v40, a2: 0x14194030CLL);
          (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v72 + 32LL))(a1: v72, a2: &v73);
          sub_1407D6070(a1: v41, a2: &v73);
          sub_140808B00(a1: &v73);
          if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v40) & 4) != 0 )
            sub_1407CD750();
        }
LABEL_92:
        v42 = v72;
        sub_1407D8AB0(a1: &v73, a2: 0x14191EB1BLL);
        (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64 *, __int64 *, volatile signed __int32 **, int))(*(_QWORD *)v42 + 216LL))(
          a1: v42,
          a2: &v75,
          a3: &qword_141B59758,
          a4: &v73,
          a5: &v76,
          a6: 1);
        v39 = v76;
        if ( v76 == nullptr )
          goto LABEL_104;
        goto LABEL_93;
      }
    }
    else
    {
      if ( v72 != nullptr && _InterlockedDecrement(v72 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v37)(a1: v37, a2: 1);
      v72 = (volatile signed __int32 *)v73;
      if ( v73 != 0 )
        goto LABEL_76;
    }
LABEL_88:
    v39 = v76;
    if ( v76 == nullptr )
      goto LABEL_104;
LABEL_93:
    if ( sub_1404B4FD0(a1: v39) != 0 )
    {
      if ( (unsigned __int8)sub_140FF3610() == 0 )
      {
        sub_1407D5DC0(a1: qword_141ABD878, a2: &v73, a3: &qword_141B5EDF0);
        sub_1407D8AB0(a1: &v75, a2: 0x1418E2C24LL);
        sub_140FF37E0(a1: v86);
        LOBYTE(v71) = 1;
        sub_1400015E0(a1: v9, a2: &v73, a3: v86, a4: &v75, a5: v71);
        sub_140808B00(a1: v86);
        v43 = 0;
        v44 = sub_140FF3610();
        if ( v44 == 0 )
        {
          v43 = 4;
          if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
          {
            v45 = &unk_141ABD978;
            while ( 1 )
            {
              v45 = (_QWORD *)v45[2];
              if ( v45 == nullptr || *v45 == 0 )
                break;
              if ( (*((_BYTE *)v45 + 28) & 1) == 0 || *((int *)v45 + 6) > 1 )
                goto LABEL_127;
            }
            v51 = sub_1407E2C90(a1: 2160);
            sub_1407E2EB0(a1: v51, a2: 1099914335, a3: 11153, a4: 1100015773, a5: 0, a6: 1);
            sub_1407E0010(a1: v51, a2: 0x1418D69DFLL);
            if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v51) & 4) != 0 )
              sub_1407CD750();
          }
        }
LABEL_127:
        v52 = (void (__fastcall ***)(_QWORD, __int64))v73;
        if ( v73 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v73 + 8)) == 0 )
          (**v52)(a1: v52, a2: 1);
        if ( v44 == 0 )
          goto LABEL_160;
      }
      sub_14083D2C0(a1: &v73);
      v53 = nullptr;
      if ( (unsigned __int8)sub_140800D80(a1: qword_141ABDFE8, a2: &unk_141ABFCB0, a3: &v73) != 0 )
        v53 = &unk_141ABD978;
      v54 = sub_140036ED0();
      LOBYTE(v55) = 1;
      if ( (unsigned __int8)sub_140FEC350(a1: v54, a2: v53, a3: v55) != 0 )
      {
        v56 = sub_140036ED0();
        if ( (unsigned __int8)sub_140FF3840(a1: v56) != 0 )
        {
          sub_1407D5DC0(a1: qword_141ABD878, a2: &v75, a3: &qword_141B5EDF0);
          sub_1407D8AB0(a1: v86, a2: 0x1418E2C24LL);
          sub_140FF37E0(a1: v92);
          sub_1400015E0(a1: v9, a2: &v75, a3: v92, a4: v86, a5: v71);
          sub_140808B00(a1: v92);
          v57 = sub_140036ED0();
          sub_140FEFE00(a1: v57);
          (*(void (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 760LL))(a1: qword_141B5AD60);
          v58 = (void (__fastcall ***)(_QWORD, __int64))v75;
          if ( v75 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v75 + 8)) == 0 )
            (**v58)(a1: v58, a2: 1);
          v43 = 0;
          goto LABEL_159;
        }
        v43 = 1;
        if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
        {
          v60 = &unk_141ABD978;
          while ( 1 )
          {
            v60 = (_QWORD *)v60[2];
            if ( v60 == nullptr || *v60 == 0 )
              break;
            if ( (*((_BYTE *)v60 + 28) & 1) == 0 || *((int *)v60 + 6) > 1 )
              goto LABEL_159;
          }
          v61 = sub_1407E2C90(a1: 2160);
          sub_1407E2EB0(a1: v61, a2: 1099914335, a3: 11172, a4: 1100015773, a5: 0, a6: 1);
          v62 = v61;
          v63 = 0x1418D6A01LL;
LABEL_157:
          sub_1407E0010(a1: v62, a2: v63);
          if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v61) & 4) != 0 )
            sub_1407CD750();
        }
      }
      else
      {
        v43 = 1;
        if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
        {
          v59 = &unk_141ABD978;
          while ( 1 )
          {
            v59 = (_QWORD *)v59[2];
            if ( v59 == nullptr || *v59 == 0 )
              break;
            if ( (*((_BYTE *)v59 + 28) & 1) == 0 || *((int *)v59 + 6) > 1 )
              goto LABEL_159;
          }
          v61 = sub_1407E2C90(a1: 2160);
          sub_1407E2EB0(a1: v61, a2: 1099914335, a3: 11166, a4: 1100015773, a5: 0, a6: 1);
          v62 = v61;
          v63 = 0x1418D6A28LL;
          goto LABEL_157;
        }
      }
LABEL_159:
      sub_14083D320(a1: &v73);
      goto LABEL_160;
    }
LABEL_104:
    if ( v72 != nullptr )
    {
      v43 = 1;
      if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
      {
        v46 = &unk_141ABD978;
        while ( 1 )
        {
          v46 = (_QWORD *)v46[2];
          if ( v46 == nullptr || *v46 == 0 )
            break;
          if ( (*((_BYTE *)v46 + 28) & 1) == 0 || *((int *)v46 + 6) > 1 )
            goto LABEL_160;
        }
        v49 = sub_1407E2C90(a1: 2160);
        sub_1407E2EB0(a1: v49, a2: 1099914335, a3: 11138, a4: 1100015773, a5: 0, a6: 1);
        v50 = sub_1407E0010(a1: v49, a2: 0x1419404CELL);
        (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v72 + 32LL))(a1: v72, a2: &v73);
        sub_1407D6070(a1: v50, a2: &v73);
        sub_140808B00(a1: &v73);
        if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v49) & 4) != 0 )
          goto LABEL_124;
      }
      goto LABEL_160;
    }
LABEL_113:
    v43 = 1;
    if ( (dword_141ABD994 & 1) != 0 && dword_141ABD990 <= 1 )
    {
      v47 = &unk_141ABD978;
      while ( 1 )
      {
        v47 = (_QWORD *)v47[2];
        if ( v47 == nullptr || *v47 == 0 )
          break;
        if ( (*((_BYTE *)v47 + 28) & 1) == 0 || *((int *)v47 + 6) > 1 )
          goto LABEL_160;
      }
      v48 = sub_1407E2C90(a1: 2160);
      sub_1407E2EB0(a1: v48, a2: 1099914335, a3: 11142, a4: 1100015773, a5: 0, a6: 1);
      sub_1407E0010(a1: v48, a2: 0x1418F36E6LL);
      if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v48) & 4) != 0 )
LABEL_124:
        sub_1407CD750();
    }
LABEL_160:
    v6 = v76;
    if ( v76 != nullptr && _InterlockedDecrement(v76) == 0 )
    {
      sub_1400532D0(a1: v6);
      sub_141750CFC(a1: v6);
    }
    v64 = v72;
    if ( v72 != nullptr && _InterlockedDecrement(v72 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v64)(a1: v64, a2: 1);
    sub_140808B00(a1: v88);
    sub_140808B00(a1: v89);
    if ( (v43 & 3) != 0 )
      goto LABEL_177;
LABEL_4:
    ++v8;
    v7 = v90;
    if ( v8 >= (v91 - v90) >> 3 )
      goto LABEL_166;
  }
  if ( !v21 )
  {
    v65 = &unk_141ABD978;
    while ( 1 )
    {
      v65 = (_QWORD *)v65[2];
      if ( v65 == nullptr || *v65 == 0 )
        break;
      if ( (*((_BYTE *)v65 + 28) & 1) == 0 || *((int *)v65 + 6) > 1 )
        goto LABEL_176;
    }
    v66 = sub_1407E2C90(a1: 2160);
    sub_1407E2EB0(a1: v66, a2: 1099914335, a3: 11105, a4: 1100015773, a5: 0, a6: 1);
    v67 = sub_1407E0010(a1: v66, a2: 0x1419414F6LL);
    v68 = sub_140835850(a1: v10, a2: 1851878757);
    sub_14083E100(a1: v68, a2: &v73);
    v69 = sub_1407D6070(a1: v67, a2: &v73);
    v6 = (volatile signed __int32 *)sub_1407E0010(a1: v69, a2: 0x141942406LL);
    sub_1407C31B0(a1: v93, a2: &v72, a3: 0);
    sub_1407D6070(a1: v6, a2: &v72);
    sub_140808B00(a1: &v72);
    sub_140808B00(a1: &v73);
    if ( (sub_1407E0380(a1: &unk_141ABD978, a2: v66) & 4) != 0 )
      sub_1407CD750();
  }
LABEL_176:
  sub_140808B00(a1: v88);
  sub_140808B00(a1: v89);
  v43 = 1;
LABEL_177:
  LOBYTE(v6) = v43 == 2;
  sub_140808B00(a1: v79);
  sub_140808B00(a1: v78);
  sub_14083ADA0(a1: &v90);
  return (unsigned int)v6;
}
