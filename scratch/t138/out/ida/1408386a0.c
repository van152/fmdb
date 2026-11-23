_DWORD *__fastcall sub_1408386A0(__int64 a1, _DWORD *a2, __int64 a3)
{
  int v7; // ebx
  __int64 v8; // rax
  int v9; // ebx
  __int64 v10; // rax
  char v11; // bl
  __int64 v12; // rax
  __int64 v13; // rax
  __int64 v14; // xmm6_8
  __int64 v15; // rax
  __int64 v16; // rax
  __int64 v17; // rbx
  __int64 v18; // rax
  int v19; // ebx
  __int64 v20; // rax
  int v21; // ebx
  __int64 v22; // rax
  __int64 v23; // rbx
  __int64 v24; // rax
  __int64 v25; // rbx
  __int64 v26; // rax
  __int64 v27; // rbx
  __int64 v28; // rax
  __int64 v29; // rbx
  __int64 v30; // rax
  int v31; // xmm6_4
  __int64 v32; // rax
  __int64 v33; // rcx
  int v34; // ebx
  __int64 v35; // r14
  __int64 v36; // rax
  __int64 v37; // rcx
  __int64 v38; // rax
  __int64 v39; // rcx
  __int64 v40; // rcx
  char v41; // [rsp+3Eh] [rbp-42h] BYREF
  unsigned __int8 v42; // [rsp+3Fh] [rbp-41h] BYREF
  int v43[4]; // [rsp+40h] [rbp-40h] BYREF
  __int64 v44; // [rsp+50h] [rbp-30h] BYREF
  __int64 v45; // [rsp+58h] [rbp-28h]
  __int64 v46; // [rsp+68h] [rbp-18h]

  v46 = -2;
  (*(void (__fastcall **)(__int64, char *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: &v41, a3: 1);
  if ( *(_DWORD *)(a1 + 16) != 0
    || ((*(void (__fastcall **)(__int64, unsigned __int8 *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: &v42, a3: 1),
        *(_DWORD *)(a1 + 16) != 0) )
  {
LABEL_3:
    *a2 = 1;
  }
  else
  {
    switch ( v42 )
    {
      case 0u:
      case 6u:
      case 7u:
        goto LABEL_6;
      case 1u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 4);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v7 = v43[0];
        v8 = sub_14083D4F0();
        LODWORD(v45) = v7;
        v44 = v8 + 40;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 2u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 4);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v9 = v43[0];
        v10 = sub_14083D4F0();
        LODWORD(v45) = v9;
        v44 = v10 + 56;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 3u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 1);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v11 = v43[0];
        v12 = sub_14083D4F0();
        LOBYTE(v45) = v11;
        v44 = v12 + 24;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 5u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 8);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v14 = *(_QWORD *)v43;
        v15 = sub_14083D4F0();
        v45 = v14;
        v44 = v15 + 120;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0xAu:
        sub_1407C9510(a1: &v44);
        sub_140839290(a1, a2: v43, a3: &v44);
        if ( v43[0] != 0 )
        {
          *a2 = 1;
          sub_140833970(a1: &v44);
          return a2;
        }
        sub_14083DDA0(a1: v43, a2: &v44);
        sub_14083DFA0(a1: a3, a2: v43);
        (*(void (__fastcall **)(_QWORD, int *))(**(_QWORD **)v43 + 16LL))(a1: *(_QWORD *)v43, a2: v43);
        sub_140833970(a1: &v44);
        goto LABEL_6;
      case 0xBu:
        sub_1407C9510(a1: &v44);
        sub_140839480(a1, a2: v43, a3: &v44);
        if ( v43[0] != 0 )
        {
          *a2 = 1;
          sub_14083B0A0(a1: &v44);
          return a2;
        }
        sub_14083DB80(a1: v43, a2: &v44);
        sub_14083DFA0(a1: a3, a2: v43);
        (*(void (__fastcall **)(_QWORD, int *))(**(_QWORD **)v43 + 16LL))(a1: *(_QWORD *)v43, a2: v43);
        sub_14083B0A0(a1: &v44);
        goto LABEL_6;
      case 0xEu:
        *(_QWORD *)v43 = *(_QWORD *)(sub_140105F10(a1: v42) + 16);
        sub_140814D80(a1, a2: &v44, a3: v43);
        if ( (_DWORD)v44 != 0 )
          goto LABEL_3;
        v16 = sub_14083D4F0();
        v45 = *(_QWORD *)v43;
        v44 = v16 + 152;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0xFu:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 8);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v17 = *(_QWORD *)v43;
        v18 = sub_14083D4F0();
        v45 = v17;
        v44 = v18 + 72;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0x11u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 1);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v19 = SLOBYTE(v43[0]);
        v20 = sub_14083D4F0();
        LODWORD(v45) = v19;
        v44 = v20 + 40;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0x12u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 2);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v21 = SLOWORD(v43[0]);
        v22 = sub_14083D4F0();
        LODWORD(v45) = v21;
        v44 = v22 + 40;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0x13u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 1);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v23 = SLOBYTE(v43[0]);
        v24 = sub_14083D4F0();
        v45 = v23;
        v44 = v24 + 72;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0x14u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 2);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v25 = SLOWORD(v43[0]);
        v26 = sub_14083D4F0();
        v45 = v25;
        v44 = v26 + 72;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0x15u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 4);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v27 = v43[0];
        v28 = sub_14083D4F0();
        v45 = v27;
        v44 = v28 + 72;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0x18u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 8);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v29 = *(_QWORD *)v43;
        v30 = sub_14083D4F0();
        v45 = v29;
        v44 = v30 + 88;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0x19u:
        (*(void (__fastcall **)(__int64, int *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: v43, a3: 4);
        if ( *(_DWORD *)(a1 + 16) != 0 )
          goto LABEL_3;
        v31 = v43[0];
        v32 = sub_14083D4F0();
        LODWORD(v45) = v31;
        v44 = v32 + 104;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        goto LABEL_6;
      case 0x1Au:
        *(_QWORD *)v43 = 0;
        sub_140814B10(a1, a2: &v44, a3: v43);
        if ( (_DWORD)v44 != 0 )
        {
          *a2 = 1;
          v33 = *(_QWORD *)v43;
          if ( *(_QWORD *)v43 != 0 && _InterlockedDecrement((volatile signed __int32 *)(*(_QWORD *)v43 - 4LL)) == 0 )
            sub_1412EC9A0(a1: v33 - 4);
        }
        else
        {
          v38 = sub_14083D4F0();
          v45 = 0;
          v39 = *(_QWORD *)v43;
          if ( *(_QWORD *)v43 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(*(_QWORD *)v43 - 4LL));
          v45 = v39;
          v44 = v38 + 136;
          sub_14083DFA0(a1: a3, a2: &v44);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
          v40 = *(_QWORD *)v43;
          if ( *(_QWORD *)v43 != 0 && _InterlockedDecrement((volatile signed __int32 *)(*(_QWORD *)v43 - 4LL)) == 0 )
            sub_1412EC9A0(a1: v40 - 4);
LABEL_6:
          *a2 = *(_DWORD *)(a1 + 16);
        }
        break;
      case 0x1Bu:
        _InterlockedIncrement((volatile signed __int32 *)(a1 + 8));
        (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)a1 + 40LL))(a1, a2: &v44, a3: 8);
        v34 = *(_DWORD *)(a1 + 16);
        v35 = v44;
        v36 = sub_14083D4F0();
        v37 = 0;
        if ( v34 == 0 )
          v37 = v35;
        v45 = v37;
        v44 = v36 + 200;
        sub_14083DFA0(a1: a3, a2: &v44);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(a1: v44, a2: &v44);
        if ( _InterlockedDecrement((volatile signed __int32 *)(a1 + 8)) == 0 )
          (**(void (__fastcall ***)(__int64, __int64))a1)(a1, a2: 1);
        goto LABEL_6;
      default:
        v13 = sub_1412EABC0(a1: v42);
        if ( v13 != 0 )
          (*(void (__fastcall **)(__int64, __int64 *, __int64, __int64, char))(*(_QWORD *)v13 + 16LL))(
            a1: v13,
            a2: &v44,
            a3,
            a4: a1,
            a5: v41);
        else
          *(_DWORD *)(a1 + 16) = 1;
        goto LABEL_6;
    }
  }
  return a2;
}
