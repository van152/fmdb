char __fastcall sub_14392D4F0(_QWORD *a1, unsigned int a2)
{
  _QWORD *v4; // r14
  int v5; // eax
  int v6; // eax
  int v7; // eax
  int v8; // eax
  _QWORD v10[5]; // [rsp+30h] [rbp-28h] BYREF

  sub_140F7EC80((unsigned int)&qword_141B5FDA8, (_DWORD)a1, qword_141B5FDC0, a2, 1, 0);
  v10[0] = a1[1];
  if ( (unsigned __int8)sub_140F7EE40((unsigned int)&qword_141B5FDA8, (unsigned int)v10, qword_141B5FE40, a2, 1, 0) != 0 )
    a1[1] = v10[0];
  v10[0] = a1[2];
  if ( (unsigned __int8)sub_140F7EE40((unsigned int)&qword_141B5FDA8, (unsigned int)v10, qword_141B5FE40, a2, 1, 0) != 0 )
    a1[2] = v10[0];
  v10[0] = a1[3];
  if ( (unsigned __int8)sub_140F7EE40((unsigned int)&qword_141B5FDA8, (unsigned int)v10, qword_141B5FE40, a2, 1, 0) != 0 )
    a1[3] = v10[0];
  v10[0] = a1[4];
  if ( (unsigned __int8)sub_140F7EE40((unsigned int)&qword_141B5FDA8, (unsigned int)v10, qword_141B5FE40, a2, 1, 0) != 0 )
    a1[4] = v10[0];
  v10[0] = a1[6];
  if ( (unsigned __int8)sub_140F7EE40((unsigned int)&qword_141B5FDA8, (unsigned int)v10, qword_141B5FE40, a2, 1, 0) != 0 )
    a1[6] = v10[0];
  v10[0] = a1[7];
  if ( (unsigned __int8)sub_140F7EE40((unsigned int)&qword_141B5FDA8, (unsigned int)v10, qword_141B5FE40, a2, 1, 0) != 0 )
    a1[7] = v10[0];
  v10[0] = a1[8];
  if ( (unsigned __int8)sub_140F7EE40((unsigned int)&qword_141B5FDA8, (unsigned int)v10, qword_141B5FE40, a2, 1, 0) != 0 )
    a1[8] = v10[0];
  sub_140F7FD40(&qword_141B5FDA8, a1 + 5, a2);
  v4 = a1 + 9;
  sub_140F7FE40(&qword_141B5FDA8, a1 + 9, a2);
  if ( *a1 != 0 )
  {
    v5 = *(_DWORD *)(*a1 + 12LL);
    if ( v5 > 135973 )
    {
      if ( v5 == 135974 )
      {
        if ( *v4 == 0 )
          goto LABEL_33;
        v8 = *(_DWORD *)(*v4 + 12LL);
        if ( v8 != 97 && v8 != 98 )
          goto LABEL_33;
      }
      else
      {
        if ( v5 != 51013962 )
          return 1;
        if ( *v4 == 0 )
          goto LABEL_33;
        v7 = *(_DWORD *)(*v4 + 12LL);
        if ( v7 != 97 && v7 != 98 )
          goto LABEL_33;
      }
LABEL_32:
      *a1 = sub_140F45DB0(qword_141B5FDC0);
      goto LABEL_33;
    }
    if ( (unsigned int)(v5 - 82) < 2 )
    {
LABEL_33:
      *v4 = 0;
      return 1;
    }
    if ( v5 == 135973 )
    {
      if ( *v4 == 0 )
        goto LABEL_33;
      v6 = *(_DWORD *)(*v4 + 12LL);
      if ( v6 != 97 && v6 != 98 )
        goto LABEL_33;
      goto LABEL_32;
    }
  }
  return 1;
}
